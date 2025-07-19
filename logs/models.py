from django.db import models
from django.core.validators import MinLengthValidator

class Log(models.Model):
    TYPE_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('debug', 'Debug'),
        ('critical', 'Critical'),
    ]
    
    CODE_CHOICES = [
        ('ERROR', 'Error'),
        ('WARNING', 'Warning'),
    ]
    
    user_id = models.IntegerField()
    platform_user_id = models.IntegerField(null=True, blank=True)
    platform_id = models.IntegerField(null=True, blank=True)
    session_id = models.IntegerField(null=True, blank=True)
    contact_id = models.IntegerField(null=True, blank=True)
    action_id = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    message = models.TextField()
    code = models.CharField(max_length=20, choices=CODE_CHOICES, null=True, blank=True)
    code_path = models.CharField(max_length=500, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.message or self.message.strip() == '':
            raise ValidationError({'message': 'Message cannot be empty'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_display()} - {self.message[:50]}..."

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

