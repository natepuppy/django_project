from django.db import models
from django.core.validators import MinLengthValidator

class Contact(models.Model):
    PROFILE_TYPE_CHOICES = [
        ('person', 'Person'),
        ('company', 'Company'),
        ('group', 'Group'),
    ]
    
    platform_user_id = models.IntegerField()
    session_id = models.IntegerField()
    external_id = models.CharField(max_length=255, null=True, blank=True)
    profile_url = models.URLField(null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    tags = models.JSONField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    profile_type = models.CharField(max_length=20, choices=PROFILE_TYPE_CHOICES, default='person')
    headline = models.CharField(max_length=500, null=True, blank=True)
    industry = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    connections_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    metadata = models.JSONField(null=True, blank=True)
    is_connection = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.connections_count < 0:
            raise ValidationError({'connections_count': 'Connections count cannot be negative'})
        if self.followers_count < 0:
            raise ValidationError({'followers_count': 'Followers count cannot be negative'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.name or f"Contact {self.id}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

