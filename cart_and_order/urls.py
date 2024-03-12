from django.urls import path
from .views import CartDetailView, OrderListView, OrderDetailView, AddToCartView, RemoveFromCartView, CreateOrderView

urlpatterns = [
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('order/', OrderDetailView.as_view(), name='order-detail'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),

]
