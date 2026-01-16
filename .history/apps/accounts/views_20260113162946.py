from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            username=request.POST['password']
        )
        
        if user:
            login(request, user)
            return redirect('dashboard')
        
    return render(request, 'accounts/login.html')

def dashborad(request):
    role = request.user.role
    
    if role == 'manager':
        return redirect('manager_dashboard')
    if role == 'lecturer':
        return redirect('lecturer_dashboard')
    if role == 'cs':
        return redirect('cs_dashboard')
    return redirect('student_dashboard')