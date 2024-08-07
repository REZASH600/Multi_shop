from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models
from django.contrib.auth import authenticate


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput
    )

    class Meta:
        model = models.User
        fields = ["phone", "email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ["email", "password", "image", "is_active", "is_admin"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput({'placeholder': 'phone or email'}))
    password = forms.CharField(widget=forms.PasswordInput({'placeholder': 'password'}))
    remember_me = forms.BooleanField(required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            if username[-10:] != '@gmail.com':
                raise ValidationError('Please enter the correct email')

        else:
            if not username.isdigit() or len(username) != 11:
                raise ValidationError('Please enter the correct phone')

        return username
