from django.dispatch import receiver
from django.db.models.signals import pre_save
from . import models


@receiver(pre_save, sender=models.Address)
def my_address_pre_save_handler(sender, instance, **kwargs):
    old_addresses = models.Address.objects.filter(user=instance.user,is_active=True)
    if old_addresses:
        old_addresses.update(is_active=False)
    
    
