from .models import Log
from datetime import timedelta
from django.utils import timezone

# calculating the date for one day ago
one_day_ago = timezone.now() - timedelta(days=1) # exact time one day ago
start_of_day = one_day_ago.replace(hour=0, minute=0, second=0, microsecond=0) # sets up start of day i.e midnight
end_of_day = one_day_ago.replace(hour=23, minute=59, second=59, microsecond=999999) # sets up end of day i.e midnight

"""
The following cron job function is used to delete all the logs
which were published a day ago so as to not hog up a lot of space.

"""

def log_clearer():
    logs_to_delete = Log.objects.all().filter(timestamp_range=(start_of_day,  end_of_day))
    logs_to_delete.delete()
    