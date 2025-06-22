from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import notify_if_out_of_stock
from .tasks import log_price_change

@receiver(post_save, sender=Product)
def check_stock(sender, instance, **kwargs):
    notify_if_out_of_stock.delay(instance.id)

@receiver(post_save, sender=Product)
def handle_product_save(sender, instance, created, **kwargs):
    if created:
        print(f"Yangi mahsulot yaratildi: {instance.name}")
    else:
        # Fon ishni chaqiramiz
        log_price_change.delay(instance.id)









