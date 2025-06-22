from celery import shared_task
from .models import Product
from django.core.mail import send_mail

@shared_task
def notify_if_out_of_stock(product_id):
    product = Product.objects.get(id=product_id)
    if product.stock == 0:
        send_mail(
            subject='Product out of stock!',
            message=f"{product.name} tugadi!",
            from_email='admin@yourshop.uz',
            recipient_list=['admin@example.com']
        )

@shared_task
def log_price_change(product_id):
    product = Product.objects.get(id=product_id)
    print(f"[TASK] Mahsulot narxi o'zgardi: {product.name} - {product.price}")


