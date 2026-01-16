from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Có mặt'),
        ('absent', 'Vắng'),
        ('late', 'Đi trễ'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)