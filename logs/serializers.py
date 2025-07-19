from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    message = serializers.CharField()
    
    def validate(self, data):
        if 'message' in data and (not data['message'] or data['message'].strip() == ''):
            raise serializers.ValidationError({'message': 'Message cannot be empty'})
        return data
    
    class Meta:
        model = Log
        # These fields will appear in the API response
        fields = [
            'id',
            'user_id',
            'platform_user_id',
            'platform_id',
            'session_id',
            'contact_id',
            'action_id',
            'type',
            'message',
            'code',
            'code_path',
            'created_at',
            'updated_at',
            'deleted_at',
        ]

        # These fields will be read-only (returned in response, ignored in input)
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
