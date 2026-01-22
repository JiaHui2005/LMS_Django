from django import forms
from .models import Subject, Syllabus, SyllabusVersion, WeeklyPlan, GradingItem

class SubjectForm(forms.ModelForm):
    
    class Meta:
        model = Subject
        fields = ['code', 'name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }
        
class SyllabusForm(forms.ModelForm):
    
    class Meta:
        model = Syllabus
        fields = ['subject', 'default_weeks']
        
class SyllabusVersionForm(forms.ModelForm):
    
    class Meta:
        model = SyllabusVersion
        fields = ['version', 'note', 'is_active']

class WeeklyPlanForm(forms.ModelForm):
    
    class Meta:
        model = WeeklyPlan
        fields = ['title', 'content', 'reference_materials']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'reference_materials': forms.Textarea(attrs={'rows': 3})
        }

class GradingItemForm(forms.ModelForm):
    
    class Meta:
        model = GradingItem
        fields = ['name', 'weight', 'week_number']
        

