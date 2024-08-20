from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models
from django.contrib.auth import login, authenticate
from django.contrib.auth.password_validation import validate_password


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

        try:
            validate_password(password1)
        except ValidationError as e:
            self.add_error("password1", e)

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password1 = forms.CharField(
        label=_("New Password"), widget=forms.PasswordInput, required=False
    )
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput, required=False
    )

    class Meta:
        model = models.User
        fields = ["email", "image", "is_active", "is_admin"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))

        try:
            if password1:
                validate_password(password1)
        except ValidationError as e:
            self.add_error("password1", e)

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password2")
        if commit:
            if password:
                print(password)
                user.set_password(password)

            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255, widget=forms.TextInput({"placeholder": "phone or email"})
    )
    password = forms.CharField(widget=forms.PasswordInput({"placeholder": "password"}))
    remember_me = forms.BooleanField(required=False)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if "@" in username:
            if username[-10:] != "@gmail.com":
                raise ValidationError("Please enter the correct email")

        else:
            if not username.isdigit() or len(username) != 11:
                raise ValidationError("Please enter the correct phone")

        return username


class RegisterForm(forms.Form):
    phone = forms.CharField(
        max_length=11, widget=forms.TextInput({"placeholder": "phone"})
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) != 11 or not phone.isdigit():
            raise ValidationError("Please enter the correct phone")

        return phone


class CheckOtpForm(forms.Form):
    random_code = forms.CharField(
        max_length=5, widget=forms.TextInput({"placeholder": "code"})
    )

    def clean_random_code(self):
        code = self.cleaned_data.get("random_code")
        if len(code) != 5 or not code.isdigit():
            raise ValidationError("Please enter the correct code")
        return code


class ForgotPasswordForm(forms.Form):
    phone_or_email = forms.CharField(
        max_length=255, widget=forms.TextInput({"placeholder": "phone or email"})
    )

    def clean(self):
        phone_or_email = self.cleaned_data.get("phone_or_email")
        if "@" in phone_or_email:
            if phone_or_email[-10:] != "@gmail.com":
                raise ValidationError("Please enter the correct email")

            if not models.User.objects.filter(email=phone_or_email).exists():
                raise ValidationError("email not found.")

        else:
            if len(phone_or_email) != 11 or not phone_or_email.isdigit():
                raise ValidationError("Please enter the correct phone")

            if not models.User.objects.filter(phone=phone_or_email).exists():
                raise ValidationError("phone not found.")


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "new password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "confirm password"})
    )

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            if password2 != password1:
                raise ValidationError("passwords must match")

            try:
                validate_password(password1)
            except ValidationError as e:
                self.add_error("password1", e)


class ProfileForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "old password"}), required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "new password"}), required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput({"placeholder": "confirm password"}), required=False
    )
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email", "image"]

    def clean(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        old_password = self.cleaned_data.get("old_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("passwords must match")

        if new_password and new_password == confirm_password == old_password:
            raise ValidationError("new password cannot be the same as the old password")

        if old_password:
            if not new_password and confirm_password:
                raise ValidationError("please enter new password")
            elif new_password and not confirm_password:
                raise ValidationError("please enter confirm password")
            elif not new_password and not confirm_password:
                raise ValidationError("please enter new password and confirm password")

        elif new_password or confirm_password:
            raise ValidationError("please enter old password .")

        try:
            if new_password:
                validate_password(new_password)
        except ValidationError as e:
            self.add_error("new_password", e)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        user = self.instance
        if old_password and not user.check_password(old_password):
            raise ValidationError("old password is incorrect.")
        return old_password

    def save(self, commit=True, request=None):
        user = super().save(commit=False)

        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)
            if commit:
                user.save()
                if request:
                    user_auth = authenticate(
                        username=request.user.phone, password=new_password
                    )
                    login(request, user_auth)

        elif commit:
            user.save()

        return user
