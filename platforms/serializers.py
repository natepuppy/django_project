from rest_framework import serializers
from .models import Platform

class PlatformSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, allow_blank=False)
    
    def validate(self, data):
        if 'name' in data and (not data['name'] or data['name'].strip() == ''):
            raise serializers.ValidationError({'name': 'Name cannot be empty'})
        return data
    
    class Meta:
        model = Platform
        # These fields will appear in the API response
        fields = [
            'id',
            'name',
            'base_url',
            'login_url',
            'has_captcha',
            'is_active',
            'created_at',
            'updated_at',
            'deleted_at',
        ]

        # These fields will be read-only (returned in response, ignored in input)
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
