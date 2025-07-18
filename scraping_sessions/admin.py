from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'platform_user_id', 'type', 'status', 'errors_count', 'ip_address', 'port', 'started_at', 'completed_at', 'created_at', 'updated_at', 'deleted_at']
    list_filter = ['type', 'status', 'created_at', 'updated_at', 'deleted_at']
    search_fields = ['platform_user_id', 'ip_address', 'port']
    list_per_page = 100
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_display_links = ['id']
