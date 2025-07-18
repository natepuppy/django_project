from rest_framework import serializers
from .models import PlatformUser

class PlatformUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, allow_blank=False)
    
    def validate(self, data):
        if 'username' in data and (not data['username'] or data['username'].strip() == ''):
            raise serializers.ValidationError({'username': 'Username cannot be empty'})
        return data
    
    class Meta:
        model = PlatformUser
        # These fields will appear in the API response
        fields = [
            'id',
            'user_id',
            'platform_id',
            'username',
            'email',
            'encrypted_password',
            'status',
            'daily_connection_request',
            'weekly_connection_request_limit',
            'daily_connection_request_count',
            'weekly_connection_request_count',
            'last_login_at',
            'created_at',
            'updated_at',
            'deleted_at',
        ]

        # These fields will be read-only (returned in response, ignored in input)
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
