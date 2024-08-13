import random
import uuid
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import render, redirect, reverse

from django.views import View
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from . import models
from django.conf import settings
from django.http import JsonResponse


class LoginView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')
        form = forms.LoginForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            next_page = request.GET.get('next_page', '/')
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)

                if cd['remember_me']:
                    request.session['username'] = cd['username']
                    request.session['password'] = cd['password']
                    request.session.set_expiry(timedelta(days=30))
                return redirect(next_page)

            message = 'User not found.'
        else:
            message = 'Invalid username or password.'

        messages.error(request, message)
        return render(request, 'account/login.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/')


class RegisterView(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('/')

        form = forms.RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            token = str(uuid.uuid4())
            random_code = random.randint(10000, 99999)

            # send code
            print(random_code)
            models.Otp.objects.update_or_create(
                phone=phone,
                defaults={'random_code': random_code, 'token': token},
                create_defaults={'phone': phone, 'token': token, 'random_code': random_code}
            )

            request.session['token'] = token
            request.session['action'] = None
            return redirect('account_app:check_otp')

        return render(request, 'account/register.html', {'form': form})


class CheckOtpView(View):
    expiry_time = int(getattr(settings, 'EXPIRY_TIME', 120))  # seconds

    def get(self, request):

        if self.request.user.is_authenticated:
            return redirect('/')

        token = request.session.get('token')
        otp = self._get_otp(token)
        if otp is None:
            action = request.session.get('action', 'register')
            if action == 'forgot_password':
                return redirect('account_app:forgot_password')
            return redirect('account_app:register')

        form = forms.CheckOtpForm()

        return render(request, 'account/check-otp.html',
                      {'form': form, 'expiry_time': self.expiry_time, 'otp_created': otp.created_at})

    def post(self, request):
        form = forms.CheckOtpForm(request.POST)
        next_page = request.POST.get('next_page', '/')
        token = request.session.get('token')

        if form.is_valid():
            code = form.cleaned_data['random_code']
            otp = self._get_otp(token, code)

            if not otp:
                return JsonResponse({'response': 'Code is not valid.'}, status=400)

            if self._is_expired(otp):
                return JsonResponse({'response': 'Code has expired.'}, status=400)

            action = request.session.get('action', 'register')
            if action == 'forgot_password':
                try:
                    user = models.User.objects.get(phone=otp.phone)
                except:
                    return JsonResponse({'response': 'User not found.'}, status=400)

                new_token = str(uuid.uuid4())
                models.PasswordResetToken.objects.update_or_create(
                    user=user,
                    defaults={'token': new_token},
                    create_defaults={'token': new_token, user: user}
                )
                request.session['reset_password_token'] = new_token
                otp.delete()
                return JsonResponse({'response': 'Success', 'redirect_url': reverse('account_app:reset_password',
                                                                                    kwargs={'token': new_token})})

            user, _ = models.User.objects.get_or_create(phone=otp.phone)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session['token'] = None
            otp.delete()
            return JsonResponse({'response': 'Success', 'redirect_url': next_page}, status=200)

        return JsonResponse({'response': form.errors.get('random_code', 'Invalid code')}, status=400)

    def _get_otp(self, token, code=None):
        try:
            if code is not None:
                return models.Otp.objects.get(token=token, random_code=code)
            return models.Otp.objects.get(token=token)

        except models.Otp.DoesNotExist:
            return None

    def _is_expired(self, otp):
        expired_time = otp.created_at + timedelta(minutes=self.expiry_time)
        return timezone.now() > expired_time


class ResendCodeView(View):
    def post(self, request):
        token = request.session.get('token')
        try:
            otp = models.Otp.objects.get(token=token)
            random_code = random.randint(10000, 99999)
            # send code
            print(random_code)
            otp.random_code = random_code

            otp.save()

            return JsonResponse({'response': 'Resend Code.', 'otpCreated': otp.created_at})
        except:
            action = request.session.get('action', 'register')
            if action == 'forgot_password':
                return redirect('account_app:forgot_password')
            return redirect('account_app:register')



