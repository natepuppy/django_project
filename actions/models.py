from django.db import models
from django.core.validators import MinLengthValidator

class Action(models.Model):
    TYPE_CHOICES = [
        ('message', 'Message'),
        ('connection_request', 'Connection Request'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
        ('error', 'Error'),
    ]
    
    platform_user_id = models.IntegerField()
    contact_id = models.IntegerField()
    session_id = models.IntegerField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='message')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message_text = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    retry_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.retry_count < 0:
            raise ValidationError({'retry_count': 'Retry count cannot be negative'})
        if self.type == 'message' and not self.message_text:
            raise ValidationError({'message_text': 'Message text is required for message type actions'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_type_display()} - {self.get_status_display()} (Contact: {self.contact_id})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

