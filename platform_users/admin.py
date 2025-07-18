from django.contrib import admin
from .models import PlatformUser

@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'platform_id', 'username', 'email', 'status', 'created_at', 'updated_at', 'deleted_at']
    list_filter = ['status', 'created_at', 'updated_at', 'deleted_at']
    search_fields = ['username', 'email', 'user_id', 'platform_id']
    list_per_page = 100
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_display_links = ['username']
