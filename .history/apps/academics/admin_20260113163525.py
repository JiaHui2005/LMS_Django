from django.contrib import admin
from .models import Attendance, Grade

# Register your models here.

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'date', 'status')
    list_filter = ('class_obj', 'status', 'date')
    search_fields = ('student__username',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'component', 'score')
    list_filter = ('class_obj', 'component')
    
