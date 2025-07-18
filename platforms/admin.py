from django.contrib import admin
from .models import Platform

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'base_url', 'login_url', 'has_captcha', 'created_at', 'updated_at', 'deleted_at']
    list_filter = ['has_captcha', 'created_at', 'updated_at', 'deleted_at']
    search_fields = ['name', 'base_url', 'login_url']
    list_per_page = 100
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_display_links = ['name']
