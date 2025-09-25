from django.utils import timezone
from django.conf import settings

def timezone_context(request):
    return {
        'current_timezone': settings.TIME_ZONE,
        'current_time': timezone.localtime(timezone.now()),
    }