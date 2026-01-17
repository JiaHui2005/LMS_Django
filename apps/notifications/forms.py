from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'target', 'is_active']
        labels = {
            'title': 'Tiêu đề',
            'content': 'Nội dung',
            'target': 'Đối tượng nhận',
            'is_active': 'Kích hoạt',
        }
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'target': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
               'class': 'form-check-input' 
            }),
        }