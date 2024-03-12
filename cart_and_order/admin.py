from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from django.utils.translation import gettext_lazy as _
from django.apps import apps

User = get_user_model()
# Obtenez l'application elle-même
app = apps.get_app_config('cart_and_order')

# Changez le nom de l'application dans l'interface d'administration
app.verbose_name = "Paniers et commandes"

class CartItemAdminInline(admin.TabularInline):
    model = CartItem
    extra = 0
    can_delete = False
    readonly_fields = ['product', 'quantity', 'price', 'promo_price', 'total_price']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price', 'promo_price', 'total_price')

    search_fields = ['product__name']

    list_filter = ['cart__user']

    readonly_fields = ['quantity', 'price', 'promo_price', 'total_price']

    def total_price(self, obj):
        return obj.total_price()

    total_price.short_description = _('Prix Total')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'final_total') 

    inlines = [CartItemAdminInline]

    def total(self, obj):
        return obj.total()
    total.short_description = _('Total')

    def final_total(self, obj):
        return obj.final_total()
    final_total.short_description = _('Final Total')

    readonly_fields = ['total', 'final_total']

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'is_delivered']
    inlines = [OrderItemInline]

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Order, OrderAdmin)
