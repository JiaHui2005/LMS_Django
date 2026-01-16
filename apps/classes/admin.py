from django.contrib import admin
from .models import Class, Enrollment

# Register your models here.

@admin.register(Class)
class AdminClass(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('is_active',)
    filter_horizontal = ('lecturers',)
    
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'joined_at')
    list_filter = ('class_obj',)
