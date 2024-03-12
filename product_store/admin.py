from django.contrib import admin
from django.utils.html import format_html
from django.apps import apps
from .models import *

# Obtenez l'application elle-même
app = apps.get_app_config('product_store')

# Changez le nom de l'application dans l'interface d'administration
app.verbose_name = "Gestion des produits"

class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1

class KeyWordInline(admin.TabularInline):
    model = KeyWord
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'promo_price', 'in_promo', 'in_stock', 'is_new', 'is_vedette')
    list_filter = ('category', 'brand', 'in_promo', 'in_stock', 'is_new')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'category', 'brand', 'description', 'average_rating')
        }),
        ('Images', {
            'fields': (('image_tag', 'image', 'image_secondary_tag', 'image_secondary'),),
        }),
        ('Prix et disponibilité', {
            'fields': ('price', 'promo_price', 'in_promo', 'in_stock')
        }),
        ('Options', {
            'fields': ('is_new', 'is_vedette')
        }),
        ('Autre', {
            'fields': ('specification', 'warranty_info', 'display', 'processor_capacity', 'camera_quality', 'memory', 'storage_capacity', 'graphics')
        }),
    )

    inlines = [KeyWordInline, AdditionalImageInline]

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image.url))

    def image_secondary_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image_secondary.url))

    image_tag.short_description = 'Image'
    image_secondary_tag.short_description = 'Image secondaire'

    readonly_fields = ('image_tag', 'image_secondary_tag')


class AdditionalImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_thumbnail')

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image.url))

    image_thumbnail.short_description = 'Image'

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(KeyWord)
admin.site.register(Product, ProductAdmin)
admin.site.register(AdditionalImage, AdditionalImageAdmin)
