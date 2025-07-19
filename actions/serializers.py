from rest_framework import serializers
from .models import Action

class ActionSerializer(serializers.ModelSerializer):
    platform_user_id = serializers.IntegerField()
    contact_id = serializers.IntegerField()
    session_id = serializers.IntegerField()
    
    def validate(self, data):
        if 'retry_count' in data and data['retry_count'] < 0:
            raise serializers.ValidationError({'retry_count': 'Retry count cannot be negative'})
        if data.get('type') == 'message' and not data.get('message_text'):
            raise serializers.ValidationError({'message_text': 'Message text is required for message type actions'})
        return data
    
    class Meta:
        model = Action
        # These fields will appear in the API response
        fields = [
            'id',
            'platform_user_id',
            'contact_id',
            'session_id',
            'type',
            'status',
            'message_text',
            'error_message',
            'executed_at',
            'retry_count',
            'created_at',
            'updated_at',
            'deleted_at',
        ]

        # These fields will be read-only (returned in response, ignored in input)
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
