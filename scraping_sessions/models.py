from django.db import models
from django.core.validators import MinLengthValidator

class Session(models.Model):
    TYPE_CHOICES = [
        ('scraping', 'Scraping'),
        ('automation', 'Automation'),
        ('monitoring', 'Monitoring'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    platform_user_id = models.IntegerField()
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='scraping')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    errors_count = models.IntegerField(default=0)
    parameters_json = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    session_cookies_json = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.errors_count < 0:
            raise ValidationError({'errors_count': 'Errors count cannot be negative'})
        if self.port and (self.port < 1 or self.port > 65535):
            raise ValidationError({'port': 'Port must be between 1 and 65535'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

