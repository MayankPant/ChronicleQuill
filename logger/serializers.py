from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        # Fields to be included in the serialization
        fields = [
            'id',
            'level',
            'event_type',
            'message',
            'service_name',
            'user',
            'ip_address',
            'timestamp',
            'metadata',
        ]
        read_only_fields = ['id', 'timestamp']  # These fields should not be modified by users

    # Validation for specific fields (e.g., IP address or log level)
    def validate_level(self, value):
        if value not in ['INFO', 'WARNING', 'ERROR', 'DEBUG']:
            raise serializers.ValidationError("Invalid log level")
        return value

    def validate_ip_address(self, value):
        # Add any custom logic for validating IP address, if necessary
        if value and not value.startswith('192.'):  # Example rule
            raise serializers.ValidationError("Invalid IP address range")
        return value

    #  validation for the entire object
    def validate(self, data):
        if data['level'] == 'ERROR' and not data['message']:
            raise serializers.ValidationError("Error logs must have a message")
        return data
