from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    platform_user_id = serializers.IntegerField()
    session_id = serializers.IntegerField()
    
    def validate(self, data):
        if 'connections_count' in data and data['connections_count'] < 0:
            raise serializers.ValidationError({'connections_count': 'Connections count cannot be negative'})
        if 'followers_count' in data and data['followers_count'] < 0:
            raise serializers.ValidationError({'followers_count': 'Followers count cannot be negative'})
        return data
    
    class Meta:
        model = Contact
        # These fields will appear in the API response
        fields = [
            'id',
            'platform_user_id',
            'session_id',
            'external_id',
            'profile_url',
            'first_name',
            'last_name',
            'name',
            'email',
            'phone',
            'tags',
            'notes',
            'profile_type',
            'headline',
            'industry',
            'location',
            'about',
            'connections_count',
            'followers_count',
            'metadata',
            'is_connection',
            'created_at',
            'updated_at',
            'deleted_at',
        ]

        # These fields will be read-only (returned in response, ignored in input)
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
