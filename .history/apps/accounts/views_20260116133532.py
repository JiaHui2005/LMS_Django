from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import models
from apps.accounts.forms import UserForm
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
            if user.role == 'cs':
                return redirect('/dashboard/cs/')
            if user.role == 'coordinator':
                return redirect('/dashboard/coordinator/')

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
@role_required('cs')
def cs_dashboard(request):
    students = User.objects.filter(role='student')
    
    student_data = []
    for s in students:
        avg_score = Grade.objects.filter(student=s).aggregate(avg=models.Avg('score'))['avg']
        absent_count = Attendance.objects.filter(student=s, status='absent').count()
        
        student_data.append({
            'student': s,
            'avg_score': avg_score,
            'absent_count': absent_count,   
        })
        
    context = {
        'student_data': student_data
    }
    
    return render(request, 'dashboard/cs.html', context)

@login_required
@role_required('coordinator')
def coordinator_dashborad(request):
    classes = Class.objects.all()
    
    data = []
    for c in classes:
        lerturer_count = c.lecturers.count()
        student_count = Enrollment.objects.filter(class_obj=c).count()
        
        data.append({
            'class': c,
            'lecturer_count': lerturer_count,
            'student_count': student_count,
            'is_valid': lerturer_count > 0 and student_count > 0
        })
        
    context = {
        'data': data
    }
    
    return render(request, 'dashboard/coordinator.html', context)

@login_required
def logout_view(request): 
    logout(request)
    return redirect('/login/')

'''
CRUD User
'''
@login_required
@role_required('manager')
def user_list(request):
    users = User.objects.all().order_by('role', 'username')
    
    context = {
        'users': users,
    }
    
    return render (request, 'manager/user_list.html', context)

@login_required
@role_required('manager')
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
        
    context = {
        'form': form,
        'tilte': 'Tạo tài khoản.'
    }
    return render(request, 'manager/user_form.html', context)

