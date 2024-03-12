from rest_framework import serializers
from .models import Cart, CartItem, PromoCode, Order, OrderItem

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ['id', 'code']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='items.all', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'promo_code', 'total', 'discount', 'final_total']

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
        read_only_fields = ['cart']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='items.all', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'items','promo_code', 'total', 'discount', 'final_total']

class CreateOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

