from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.account.models import User


class Province(models.Model):
    name = models.CharField(_("name"), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("provinces")


class City(models.Model):
    name = models.CharField(_("name"), max_length=100)
    province = models.ForeignKey(
        Province,
        related_name="cities",
        on_delete=models.CASCADE,
        verbose_name=_("province"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("City")


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s", verbose_name=_("user")
    )
    recipient_name = models.CharField(_("recipient name"), max_length=255)
    street = models.CharField(_("stree name"), max_length=255)
    postal_code = models.CharField(_("postal code"), max_length=20)
    building_number = models.CharField(_("building number"), max_length=10)
    unit = models.CharField(_("unit"), max_length=10, blank=True, null=True)
    full_address = models.CharField(
        _("full address"), max_length=255, null=True, blank=True
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="%(class)s", verbose_name=_("city")
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name="%(class)s",
        verbose_name=_("province"),
    )
    is_active = models.BooleanField(_("is active"), default=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        if self.full_address:
            return f"{self.recipient_name} - {self.full_address}"
        address_parts = [self.building_number]
        if self.unit:
            address_parts.append(f"Unit {self.unit}")
        address_parts.append(self.street)
        return f"{self.recipient_name} - {', '.join(address_parts)}, {self.city.name}, {self.city.province.name}"

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
