from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    platform_user_id = serializers.IntegerField()
    
    def validate(self, data):
        if 'errors_count' in data and data['errors_count'] < 0:
            raise serializers.ValidationError({'errors_count': 'Errors count cannot be negative'})
        if 'port' in data and data['port'] and (data['port'] < 1 or data['port'] > 65535):
            raise serializers.ValidationError({'port': 'Port must be between 1 and 65535'})
        return data
    
    class Meta:
        model = Session
        # These fields will appear in the API response
        fields = [
            'id',
            'platform_user_id',
            'started_at',
            'completed_at',
            'type',
            'status',
            'errors_count',
            'parameters_json',
            'ip_address',
            'port',
            'session_cookies_json',
            'created_at',
            'updated_at',
            'deleted_at',
        ]

        # These fields will be read-only (returned in response, ignored in input)
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
