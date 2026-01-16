from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from common.decorators import role_required
from apps.accounts.models import User
from apps.classes.models import Class, Enrollment
from apps.academics.models import Grade, Attendance
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        print("METHOD:", request.method)
        print("USER:", user)

        if user is not None:
            login(request, user)

            if user.role == 'manager':
                return redirect('/dashboard/manager/')
            if user.role == 'student':
                return redirect('/dashboard/student/')
            if user.role == 'lecturer':
                return redirect('/dashboard/lecturer/')
            if user.role == 'student':
                return redirect('/')

        return render(request, 'accounts/login.html', {
            'error': 'Sai tài khoản hoặc mật khẩu'
        })

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
    
    total_user = User.objects.count()
    total_students = User.objects.filter(role='student').count()
    total_lecturers = User.objects.filter(role='lecturer').count()
    total_classes = Class.objects.count()
    
    context = {
        'total_users': total_user,
        'total_classes': total_classes,
        'total_students': total_students,
        'total_lecturers': total_lecturers,
    }
    
    return render(request, 'dashboard/manager.html', context)

@login_required
@role_required('student')
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    
    grades = Grade.objects.filter(student=request.user)
    attendance = Attendance.objects.filter(student=request.user)
    
    context = {
        'enrollments': enrollments,
        'grades': grades,
        'attendance': attendance,
    }
    
    return render(request, 'dashboard/student.html', context)

@login_required
@role_required('lecturer')
def lecturer_dashboard(request):
    classes = Class.objects.filter(lecturers=request.user).distinct()
    
    total_classes = classes.count()
    total_student = Enrollment.objects.filter(
        class_obj__in=classes
    ).values('student').distinct().count()

    context = {
        'classes': classes,
        'total_classes': total_classes,
        'total_student': total_student,
    }
    
    return render(request, 'dashboard/lecturer.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')