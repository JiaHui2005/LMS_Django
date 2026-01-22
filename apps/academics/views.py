from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from .models import Attendance, Grade, SyllabusVersion
from apps.classes.models import Enrollment, Class
from datetime import date

# Giang vien diem danh
@login_required
@role_required('lecturer')
def take_attendance(request, class_id):
    enrollments = Enrollment.objects.filter(class_obj_id=class_id)

    if request.method == 'POST':
        for e in enrollments:
            status = request.POST.get(f'status_{e.student.id}')
            Attendance.objects.update_or_create(
                student=e.student,
                class_obj_id=class_id,
                date=date.today(),
                defaults={'status': status}
            )
        return redirect('lecturer_classes')

    return render(request, 'academics/attendance.html', {
        'enrollments': enrollments
    })

# Giang vien nhap diem
@login_required
@role_required('lecturer')
def enter_grade(request, class_id):
    enrollments = Enrollment.objects.filter(class_obj_id=class_id)

    if request.method == 'POST':
        for e in enrollments:
            score = request.POST.get(f'score_{e.student.id}')
            Grade.objects.update_or_create(
                student=e.student,
                class_obj_id=class_id,
                component='final',
                defaults={'score': score}
            )
        return redirect('lecturer_classes')

    return render(request, 'academics/grade.html', {
        'enrollments': enrollments
    })
       
# Sinh vien xem lop hoc cua chinh minh
@login_required
@role_required('student')
def my_classes(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('class_obj')
    
    context = {
        'enrollments': enrollments
    }
    
    return render(request, 'student/class_list.html', context)
    
# Sinh vien xem chi tiet lop hoc
@login_required
@role_required('student')
def class_detail(request, class_id):
    enrollment = get_object_or_404(Enrollment, student=request.user, class_obj_id=class_id)
    
    classroom = enrollment.class_obj
    lecturers = classroom.lecturers
    
    context = {
        'enrollment': enrollment,
        'classroom': classroom,
        'lecturers': lecturers
    }
    
    return render(request, 'student/class_detail.html', context)

# Quan ly xem syllabus cua lop hoc    
@login_required
@role_required('manager')
def manager_view_class_syllabus(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    
    syllabus_version = class_obj.syllabus_version
    
    context = {
        'class_obj': class_obj,
        'syllabus_version': syllabus_version,
        'weeks': syllabus_version.weeks.all() if syllabus_version else [],
        'grading_items': syllabus_version.grading_item.all() if syllabus_version else []
    }
    
    return render(request, 'manager/syllabus_detail.html', context)

# Lec chinh sua syllabus cua lop hoc
@login_required
@role_required('lecturer')
def lecturer_edit_class_syllabus(request, class_id):
    class_obj = get_object_or_404(Class, id=class_obj, lecturer=request.user)
    
    syllabus_version = class_obj.syllabus_version
    
    if not syllabus_version:
        
        return render(request, 'lecturer/no_syllabus.html', {'class_obj': class_obj})
    
    weeks = syllabus_version.weeks.all()
    
    if request.method == 'POST':
        for week in weeks:
            week.title = request.POST.get(f"title_week{week.id}", week.title)
            week.content = request.POST.get(f"content_week{week.id}", week.content)
            week.reference_materials = request.POST.get(f"reference_materials_week{week.id}", week.reference_materials)
            week.save()
            
        return redirect('lecturer_edit_class_syllabus', class_id=class_obj.id)
    
    context = {
        'class_obj': class_obj,
        'syllabus_version': syllabus_version,
        'weeks': weeks
    }
    
    return render(request, 'lecturer/syllabus_edit.html', context)
    
    
    
    