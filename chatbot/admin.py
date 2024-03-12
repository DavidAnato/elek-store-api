# admin.py

from django.contrib import admin
from .models import Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'response', 'timestamp']
    search_fields = ['user__username', 'message', 'response']
    list_filter = ['timestamp']
