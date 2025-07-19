from django.contrib import admin
from .models import Action

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['id', 'platform_user_id', 'contact_id', 'session_id', 'type', 'status', 'retry_count', 'executed_at', 'created_at', 'updated_at', 'deleted_at']
    list_filter = ['type', 'status', 'created_at', 'updated_at', 'deleted_at']
    search_fields = ['platform_user_id', 'contact_id', 'session_id', 'message_text']
    list_per_page = 100
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_display_links = ['id']
