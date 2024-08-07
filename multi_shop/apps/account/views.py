from datetime import timedelta

from django.shortcuts import render, redirect

from django.views import View
from . import forms
from django.contrib.auth import login, authenticate
from django.contrib import messages


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
