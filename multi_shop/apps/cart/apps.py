from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.cart"
    verbose_name = _("Cart")
    verbose_name_plural = _('Carts')
