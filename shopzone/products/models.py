from django.db import models
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    discount_percent = models.PositiveIntegerField(default=0)  # 0-100 oralig‘ida chegirma

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # ✅ 1. Chegirmali narxni hisoblash
    def get_discounted_price(self):
        """
        Mahsulotga chegirma bor bo‘lsa, narxni hisoblab beradi.
        """
        if self.discount_percent:
            discount_amount = self.price * Decimal(self.discount_percent / 100)
            return self.price - discount_amount
        return self.price

    # ✅ 2. Mahsulot stokda bormi?
    def is_in_stock(self):
        """
        Mahsulot mavjudligini bildiradi.
        """
        return self.stock > 0

    # ✅ 3. Mahsulot chegirmada ekanligini bildiradi
    def is_discounted(self):
        return self.discount_percent > 0

    # ✅ 4. Qisqacha info (masalan admin panel yoki API uchun)
    def short_info(self):
        return f"{self.name} - ${self.price} ({'chegirmali' if self.is_discounted() else 'normal'})"

    # ✅ 5. Narx formatlangan holda (frontend ko‘rinishi uchun qulay)
    def formatted_price(self):
        return f"${self.price:.2f}"

    # ✅ 6. Chegirma matni (ko‘rsatish uchun)
    def discount_label(self):
        if self.is_discounted():
            return f"{self.discount_percent}% OFF"
        return "No discount"

    # ✅ 7. Mahsulot zaxirasini to‘ldirish (admin yoki supplier uchun)
    def replenish(self, quantity):
        """
        Mahsulot zaxirasini (stock) to‘ldiradi.
        Masalan, ombordan yangi mahsulotlar kelganda chaqiriladi.
        """
        if quantity > 0:
            self.stock += quantity
            self.save()
        else:
            raise ValueError("To‘ldiriladigan miqdor musbat bo‘lishi kerak.")















