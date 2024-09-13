from django.contrib import admin
from . import models


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["recipient_name", "street", "city", "postal_code", "is_active"]
    list_filter = ["city", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["recipient_name", "street", "postal_code", "city__name"]


admin.site.register(models.Province)
admin.site.register(models.City)
