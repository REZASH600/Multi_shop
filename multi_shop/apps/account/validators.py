import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models


class PasswordValidator:
    """
    Custom password validator to enforce specific password rules.
    """

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Password must be at least 8 characters long."),
                code="password_too_short",
            )

        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
            raise ValidationError(
                _("Password must contain both letters and numbers."),
                code="password_no_letter_or_digit",
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code="password_no_special_char",
            )

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long, contain letters, "
            "numbers, and at least one special character."
        )


def validate_phone(phone):
    """
    Validates the phone number. Ensures it is composed of digits and is 11 characters long.
    """
    if not phone.isdigit() or len(phone) != 11:
        raise ValidationError(_("Enter a valid phone number with 11 digits."))


def validate_email(email=None,phone=None):
    """
    Validates the email address. Ensures it is in a valid email format.
    """
    if email:
        user_obj = models.User.objects.filter(email=email)
        if user_obj.exists():
            if user_obj[0].phone != phone:
                raise ValidationError(_("email already exists."))

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValidationError(_("Enter a valid email address."))
