from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from common.decorators import role_required
from .models import Class, Enrollment
from .forms import ClassForm

# Lay lop hoc ma giang vien dang day
@login_required
@role_required('lecturer')
def lecturer_classes(request):
    classes = Class.objects.filter(lecturers=request.user)
    
    context = {
        'classes': classes
    }
    
    return render(request, 'classes/lecturer_classes.html', context)

# Lay danh sach lop hoc
@login_required
@role_required('manager')
def class_list(request):
    classes = Class.objects.all().order_by('-id')
    
    context = {
        'classes': classes
    }
    
    return render(request, 'manager/class_list.html', context)

# Tao lop hoc
@login_required
@role_required('manager')
def class_create(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Tạo lớp học thành công."
            )
            return redirect('class_list')
    else:
        form = ClassForm()
        
    context = {
        'form': form,
        'title': 'Tạo lớp học'
    }
    
    return render(request, 'manager/class_form.html', context)

# Chinh sua lop hoc
@login_required
@role_required('manager')
def class_edit(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Cập nhật lớp học thành công."
            )
            return redirect('class_list')
        else:
            print(form.errors)
    else:
        form = ClassForm(instance=class_obj)
        
    context = {
        'form': form,
        'title': 'Chỉnh sửa lớp học.'
    }
    
    return render(request, 'manager/class_form.html', context)

# Ket thuc lop hoc
@login_required
@role_required('manager')
def class_deactivate(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    class_obj.is_active = False
    class_obj.save()
    
    messages.warning(
        request,
        'Lớp học đã kết thúc.'
    )
    
    return redirect('class_list')

# Xem danh sach lop hoc co the dang ky
@login_required
@role_required('student')
def enroll_list(request):
    enrolled = Enrollment.objects.filter(
        student=request.user
    ).values_list('class_obj_id', flat=True)
    
    classes = Class.objects.filter(
        is_active=True
    ).exclude(id__in=enrolled)
    
    context = {
        'classes': classes
    }

    return render(request, 'student/enroll.html', context)

# Sinh vien tham gia lop
@login_required
@role_required('student')
def enroll_class(request, class_id):
    classroom = get_object_or_404(Class, id=class_id, is_active=True)
    
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        class_obj=classroom
    )
    
    if not created:
        messages.warning(
            request,
            'Bạn đã đăng ký lớp này rồi.'
        )
        
    else:
        messages.success(
            request,
            'Đăng ký lớp học thành công.'
        )
        
        return redirect('student_my_classes')
    
# Chi tiet lop hoc cho Lec
@login_required
@role_required('lecturer')
def lecturer_class_detail(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id, lecturers=request.user)
    
    students = (class_obj.enrollments.select_related('student').all())
    
    context = {
        'class_obj': class_obj,
        'students': students,
        'syllabus_version': class_obj.syllabus_version
    }
    
    return render(request, 'lecturer/class_detail.html', context)