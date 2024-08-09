import random
import uuid
from datetime import timedelta

from django.shortcuts import render, redirect

from django.views import View
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from . import models


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

            models.Otp.objects.create(phone=phone, token=token, random_code=random_code)
            request.session['token'] = token
            return redirect('account_app:check_otp')

        return render(request, 'account/register.html', {'form': form})
