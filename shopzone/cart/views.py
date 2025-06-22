from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404

User = Cart._meta.get_field('user').related_model

# ✅ 1. Foydalanuvchining savatchasini olish
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

# ✅ 2. Savatchaga mahsulot qo‘shish
class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

# ✅ 3. Savatchadan mahsulotni o‘chirish
class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        cart_item.delete()
        return Response({"detail": "Mahsulot savatchadan o‘chirildi."}, status=status.HTTP_204_NO_CONTENT)


from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer

class CheckoutView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        items = cart.items.all()

        if not items.exists():
            return Response({"detail": "Savatcha bo‘sh."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=user)
        total = 0

        for item in items:
            if item.product.stock < item.quantity:
                return Response({
                    "detail": f"{item.product.name} uchun yetarli mahsulot yo‘q. Qolgan: {item.product.stock}"
                }, status=status.HTTP_400_BAD_REQUEST)

            item.product.stock -= item.quantity
            item.product.save()

            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
                total_price=item.product.price * item.quantity
            )

            total += order_item.total_price

        order.total_price = total
        order.save()

        # Savatchani tozalash
        items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)








