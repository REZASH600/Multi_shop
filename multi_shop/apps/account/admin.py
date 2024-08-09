from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from . import models


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone", "email", "is_admin", "show_image"]
    list_filter = ["is_admin", "is_active"]
    fieldsets = [
        (None, {"fields": ["phone", "email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name", "image"]}),
        ("Permissions", {"fields": ["is_admin", "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["phone", "email"]
    ordering = ["phone"]
    list_editable = ["is_admin"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(models.Otp)