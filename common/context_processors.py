from django.db.models import Q
from apps.notifications.models import NotificationUser, Notification

def unread_notification_count(request):
    if not request.user.is_authenticated:
        return {}

    total = Notification.objects.filter(
        is_active=True
    ).filter(
        Q(target='all') | Q(target=request.user.role)
    ).count()

    read = NotificationUser.objects.filter(
        user=request.user,
        is_read=True
    ).count()

    return {
        'unread_notification_count': max(total - read, 0)
    }
