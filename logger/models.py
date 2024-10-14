from django.db import models

class Log(models.Model):
    # Log Levels (Info, Warning, Error, etc.)
    LOG_LEVELS = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('DEBUG', 'Debug'),
    ]

    # Type of event (can be expanded or modified as needed)
    EVENT_TYPES = [
        ('USER_ACTION', 'User Action'),
        ('SYSTEM_EVENT', 'System Event'),
        ('AUTH_EVENT', 'Authentication Event'),
        ('TASK_EVENT', 'Task Event'),
    ]

    level = models.CharField(max_length=10, choices=LOG_LEVELS, default='INFO')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='SYSTEM_EVENT')
    message = models.TextField()  # Main log message
    service_name = models.CharField(max_length=100)  # Name of the service generating the log
    user = models.CharField(max_length=100, null=True, blank=True)  # Optional, can be a username or ID
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Optional IP address
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp when log was created
    metadata = models.JSONField(null=True, blank=True)  # Optional field for additional structured data (requires PostgreSQL)

    def __str__(self):
        return f"{self.timestamp} - {self.level} - {self.service_name}: {self.message[:50]}"

    class Meta:
        ordering = ['-timestamp']  # Order logs by most recent
        indexes = [
            models.Index(fields=['level']),
            models.Index(fields=['event_type']),
            models.Index(fields=['timestamp']),
        ]

