from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, phone, email=None, password=None):
        """
        Creates and saves a User with the given phone, email and password.
        """
        if email:
            email = self.normalize_email(email)

        user = self.model(
            phone=phone,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None):
        """
        Creates and saves a superuser with the given phone, email and password.
        """

        user = self.create_user(
            phone=phone,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = models.CharField(_("phone"), max_length=11, unique=True)

    email = models.EmailField(
        _("email address"),
        max_length=255,
        null=True,
        blank=True
    )
    first_name = models.CharField(_("first name"), max_length=100, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, null=True, blank=True)
    image = models.ImageField(_("image"), upload_to='user/images', default='user/images/images.jpeg')
    is_active = models.BooleanField(_("is admin"), default=True)
    is_admin = models.BooleanField(_("is active"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.phone

    def show_image(self):
        return format_html(f"<img src='{self.image.url}' width='25px' height='25px'>")

    show_image.short_description = _("image")

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return None

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')