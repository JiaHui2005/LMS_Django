from django.db import models
from apps.classes.models import Class

# Create your models here.

class ClassSchedule(models.Model):
    DAY_CHOICES = (
        (0, 'Thứ 2'),
        (1, 'Thứ 3'),
        (2, 'Thứ 4'),
        (3, 'Thứ 5'),
        (4, 'Thứ 6'),
        (5, 'Thứ 7'),
        (6, 'Chủ nhật'),
    )
    
    STATUS_CHOICES = (
        ('scheduled', 'Đã lên lịch'),
        ('cancelled', 'Giảng viên vắng'),
        ('makeup', 'Buổi bù'),
    )
    
    classroom = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    
    day_of_week = models.IntegerField(
        verbose_name="Thứ",
        choices= DAY_CHOICES
    )
    
    start_time = models.TimeField(verbose_name="Giờ bắt đầu")
    end_time = models.TimeField(verbose_name="Giờ kết thúc")
    
    room = models.CharField(
        max_length=50,
        verbose_name="Phòng học"
    )
    
    date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày bắt đầu học"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    
    absence_reason = models.TextField(
        blank=True,
        null=True,
        help_text="Lý do giảng viên vắng (nếu có)"
    )
    
    def __str__(self):
        return f"{self.classroom.name} - {self.get_day_of_week_display()}"
