from django import forms
from apps.accounts.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'role', 'is_active']
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        qs = User.objects.filter(username=username)
        
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise forms.ValidationError("Tên đăng nhập đã được sử dụng")    
    
    def save(self, commit = True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password:
            user.set_password(password)
            
        if commit:
            user.save()
            
        return user
            