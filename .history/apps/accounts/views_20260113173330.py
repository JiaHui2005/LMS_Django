from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from common.decorators import role_required
from apps.accounts.models import User
from apps.classes.models import Class, Enrollment
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
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

def home(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.user.role == 'manager':
        return redirect('/dashboard/manager/')
    if request.user.role == 'lecturer':
        return redirect('/classes/lecturer/')
    return redirect('/login/')


@login_required
@role_required('manager')
def manager_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_classes': Class.objects.count(),
        'total_students': User.objects.filter(role='student').count(),
        'total_lecturers': User.objects.filter(role='lecturer').count(),
    }
    
    return render(request, 'dashboard/manager.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')