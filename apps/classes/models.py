from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Class(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    lecturers = models.ManyToManyField(
        User,
        related_name='teaching_classes',
        limit_choices_to={'role': 'lecturer'}
    )
    
    max_students = models.PositiveIntegerField(
        verbose_name="Sĩ số tối đa"
    )
    
    total_sessions = models.PositiveIntegerField(
        verbose_name="Tổng số buổi học"
    )
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    joined_at = models.DateField(auto_now_add=True)