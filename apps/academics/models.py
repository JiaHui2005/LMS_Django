from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
class Syllabus(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='syllabi'
    )
    
    default_week = models.PositiveIntegerField(
        help_text="Số tuần chuẩn (10 / 15/ ...)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Syllabus - {self.subject.name} ({self.default_week} tuần)"

class SyllabusVersion(models.Model):
    syllabus = models.ForeignKey(
        Syllabus,
        on_delete=models.Case,
        related_name='versions'
    )
    
    version = models.CharField(
        max_length=20,
        help_text="VD: v1.0, v1.1"
    )
    
    note = models.CharField(
        max_length=255,
        blank=True
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='created_syllabus_version'
    )
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('syllabus', 'version')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.syllabus.subject.name} - {self.version}"
    
class WeeklyPlan(models.Model):
    syllabus_version = models.ForeignKey(
        SyllabusVersion,
        on_delete=models.CASCADE,
        related_name='weeks'
    )
    
    week_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    reference_materials = models.TextField(
        blank=True,
        help_text="Link, sách, tài liệu tham khảo"
    )
    
    class Meta:
        unique_together = ('syllabus_version', 'week_number')
        ordering = ['week_number']

    def __str__(self):
        return f"Tuần {self.week_number}: {self.title}"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Có mặt'),
        ('absent', 'Vắng'),
        ('late', 'Đi trễ'),
    )
    
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    
    class_obj = models.ForeignKey(
        'classes.Class',
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    
    week_number = models.PositiveIntegerField()
    date = models.DateField()
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )
    
    class Meta:
        unique_together = ('student', 'class_obj', 'week_number')
        ordering = ['week_number']
        
    def __str__(self):
        return f"{self.student} - {self.class_obj} - Tuần {self.week_number}"
    
    
class GradingItem(models.Model):
    syllabus_version = models.ForeignKey(
        SyllabusVersion,
        on_delete=models.CASCADE,
        related_name='grading_items'
    )
    
    name = models.CharField(
        max_length=100,
        help_text="VD: Midterm, Final, Lab1"
    )
    
    weight = models.FloatField(
        help_text="Trọng số của các cột điểm"
    )
    
    week_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Thuộc tuần nào nếu có"
    )
    
    class Meta:
        ordering = ['week_number', 'name']

    def __str__(self):
        return f"{self.name} ({self.weight}%)"    
    
class Grade(models.Model):
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='grades'
    )
    
    class_obj = models.ForeignKey(
        'classes.Class',
        on_delete=models.CASCADE,
        related_name='grades'
    )
    
    grading_item = models.ForeignKey(
        GradingItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='grades'
    )
    
    score = models.FloatField()
    component = models.CharField(
        max_length=50,
        blank=True
    )
    
    class Meta:
        unique_together = ('student', 'class_obj', 'grading_item')

    def __str__(self):
        return f"{self.student} - {self.score}"
