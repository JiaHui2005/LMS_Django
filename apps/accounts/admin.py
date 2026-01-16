from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'fullname', 'role', 'is_activated')
    list_filter = ('role', 'is_activated')
    search_fields = ('username', 'fullname')
    ordering = ('role',)