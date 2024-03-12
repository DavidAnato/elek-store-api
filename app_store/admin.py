from django.contrib import admin
from django.utils.html import format_html
from django.apps import apps
from .models import *

# Obtenez l'application elle-même
app = apps.get_app_config('app_store')

# Changez le nom de l'application dans l'interface d'administration
app.verbose_name = "Gestions des applications"

class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1

class KeyWordInline(admin.TabularInline):
    model = KeyWord
    extra = 5

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'developer', 'price', 'promo_price', 'in_promo', 'is_new')
    list_filter = ('category', 'developer', 'in_promo', 'is_new')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'category', 'developer', 'description', 'average_rating')
        }),
        ('files', {
            'fields': ('installation_file', 'download_link', 'image_tag', 'image')
        }),
        ('Prix et disponibilité', {
            'fields': ('price', 'promo_price', 'in_promo',)
        }),
        ('Options', {
            'fields': ('is_new',)
        }),
    )

    inlines = [KeyWordInline, AdditionalImageInline]

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image.url))


    image_tag.short_description = 'Image'

    readonly_fields = ('image_tag',)


class AdditionalImageAdmin(admin.ModelAdmin):
    list_display = ('application', 'image_thumbnail')

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image.url))

    image_thumbnail.short_description = 'Image'

admin.site.register(Category)
admin.site.register(Developer)
admin.site.register(KeyWord)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(AdditionalImage, AdditionalImageAdmin)
