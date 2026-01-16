from django.db import models
from django.conf import settings
from apps.classes.models import Class
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
    
    
class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    score = models.FloatField()
    component = models.CharField(max_length=50)  # midterm, final, homework
