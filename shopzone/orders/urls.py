from django.urls import path
from .views import OrderCreateView, MyOrdersListView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create-order'),
    path('my-orders/', MyOrdersListView.as_view(), name='my-orders'),
]


