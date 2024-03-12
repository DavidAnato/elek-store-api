from django.contrib import admin
from .models import Contact, SkillDomain
from django.apps import apps

# Obtenez l'application elle-même
app = apps.get_app_config('digitalcontact')

# Changez le nom de l'application dans l'interface d'administration
app.verbose_name = "Contacts"

class SkillDomainAdmin(admin.ModelAdmin):
    list_display = ['name']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'professions', 'description']
    search_fields = ['user__username', 'professions', 'description']

admin.site.register(SkillDomain, SkillDomainAdmin)
admin.site.register(Contact, ContactAdmin)
