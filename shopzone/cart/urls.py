from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView
from .views import CheckoutView


urlpatterns = [
    path('', CartDetailView.as_view(), name='cart-detail'),
    path('add/', AddToCartView.as_view(), name='cart-add'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='cart-remove'),
    path('checkout/', CheckoutView.as_view(), name='cart-checkout'),

]



