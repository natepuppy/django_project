from django.db import models
from django.core.validators import MinLengthValidator

class PlatformUser(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    user_id = models.IntegerField()
    platform_id = models.IntegerField()
    username = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    email = models.EmailField()
    encrypted_password = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    daily_connection_request = models.IntegerField(default=0)
    weekly_connection_request_limit = models.IntegerField(default=0)
    daily_connection_request_count = models.IntegerField(default=0)
    weekly_connection_request_count = models.IntegerField(default=0)
    
    last_login_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.username or self.username.strip() == '':
            raise ValidationError({'username': 'Username cannot be empty'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

