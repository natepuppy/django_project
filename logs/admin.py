from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'type', 'code', 'message', 'created_at', 'updated_at', 'deleted_at']
    list_filter = ['type', 'code', 'created_at', 'updated_at', 'deleted_at']
    search_fields = ['user_id', 'message', 'code_path']
    list_per_page = 100
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_display_links = ['id']
