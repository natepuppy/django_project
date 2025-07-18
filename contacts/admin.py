from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'platform_user_id', 'session_id', 'first_name', 'last_name', 'name', 'email', 'profile_type', 'is_connection', 'connections_count', 'followers_count', 'created_at', 'updated_at', 'deleted_at']
    list_filter = ['profile_type', 'is_connection', 'created_at', 'updated_at', 'deleted_at']
    search_fields = ['first_name', 'last_name', 'name', 'email', 'external_id', 'platform_user_id']
    list_per_page = 100
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_display_links = ['id']
