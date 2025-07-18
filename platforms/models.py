from django.db import models
from django.core.validators import MinLengthValidator

class Platform(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    base_url = models.CharField(max_length=100)
    login_url = models.CharField(max_length=100)
    has_captcha = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.name or self.name.strip() == '':
            raise ValidationError({'name': 'Name cannot be empty'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'

