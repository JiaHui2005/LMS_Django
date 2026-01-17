from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    TARGET_CHOICES = (
        ('all', 'Tất cả'),
        ('manager', 'Manager'),
        ('lecturer', 'Giảng viên'),
        ('student', 'Học viên'),
        ('tc', 'Điều phối'),
        ('cs', 'CS'),
    )
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    target = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES,
        default='all'
    )
    
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_notifications'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class NotificationUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification_users'
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='user_statuses'
    )

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'notification')