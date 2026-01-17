from django import forms
from .models import ClassSchedule

class ClassScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['day_of_week', 'start_time', 'end_time', 'room']
        widgets = {
            'day_of_week': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'room': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }
        
    def clean(self):
        cleaned_data = super().clean()
    
        day = cleaned_data.get('day_of_week')
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        room = cleaned_data.get('room')
    
        if day is None:
            self.add_error('day_of_week', 'Chưa chọn thứ trong tuần.')
    
        if not room:
            self.add_error('room', 'Chưa nhập phòng học.')
    
        if not start:
            self.add_error('start_time', 'Chưa nhập giờ bắt đầu.')
    
        if not end:
            self.add_error('end_time', 'Chưa nhập giờ kết thúc.')
    
        if start and end and start >= end:
            self.add_error('end_time', 'Giờ kết thúc phải lớn hơn giờ bắt đầu.')
    
        return cleaned_data

from django import forms

class BulkScheduleForm(forms.Form):
    day_of_week = forms.ChoiceField(
        choices=ClassSchedule.DAY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    room = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    total_sessions = forms.IntegerField(
        min_value=1,
        max_value=50,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('start_time') >= cleaned_data.get('end_time'):
            raise forms.ValidationError(
                "Giờ kết thúc phải lớn hơn giờ bắt đầu."
            )
        return cleaned_data

class ScheduleStatusForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['status', 'absence_reason']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'absence_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        reason = cleaned_data.get('absence_reason')

        if status == 'cancelled' and not reason:
            self.add_error(
                'absence_reason',
                'Vui lòng nhập lý do giảng viên vắng.'
            )

        return cleaned_data
    
class MakeupScheduleForm(forms.ModelForm):
    class Meta:
        model = ClassSchedule
        fields = ['date', 'start_time', 'end_time', 'room']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'room': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start and end and start >= end:
            self.add_error(
                'end_time',
                'Giờ kết thúc phải lớn hơn giờ bắt đầu.'
            )

        return cleaned_data
