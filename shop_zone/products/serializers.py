from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()
    discount_text = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description',
            'price', 'discount_percent',
            'discounted_price', 'in_stock',
            'status_label', 'discount_text',
            'stock', 'created_at', 'updated_at'
        ]

    def get_discounted_price(self, obj):
        """Mahsulotning chegirmali narxi"""
        if obj.discount_percent:
            discount = obj.price * obj.discount_percent / 100
            return round(obj.price - discount, 2)
        return obj.price

    def get_in_stock(self, obj):
        """Mahsulot bor-yo‘qligini bildiradi"""
        return obj.stock > 0

    def get_status_label(self, obj):
        """Frontend uchun label (masalan badge)"""
        if obj.stock == 0:
            return "Tugagan"
        elif obj.discount_percent:
            return f"Chegirma {obj.discount_percent}%"
        return "Yangi"

    def get_discount_text(self, obj):
        """Chegirma haqida foydalanuvchiga ko‘rsatiladigan matn"""
        if obj.discount_percent > 0:
            return f"{obj.discount_percent}% chegirma mavjud!"
        return "Chegirma yo‘q"



