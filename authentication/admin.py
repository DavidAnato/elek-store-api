from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser
from django.utils.translation import gettext_lazy as _


admin.site.site_header = _("Site d'Administration d'Elek-store")
admin.site.site_title = _("Administration d'Elek-store")
admin.site.index_title = _("Tableau de Bord")
# admin.site.site_header_background = "/path/to/logo.png"


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'photo_tag']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_photo', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('photo_tag',)

    def photo_tag(self, obj):
        if obj.profile_photo:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.profile_photo.url))
        else:
            return "No photo"
    photo_tag.short_description = 'Photo de profil'

admin.site.register(CustomUser, CustomUserAdmin)
