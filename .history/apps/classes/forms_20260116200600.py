from django import forms
from .models import Class

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        feilds = ['code', 'name', 'lecturers', 'is_active']
        widgets = {
            'lecturers': forms.CheckboxSelectMultiple
        }