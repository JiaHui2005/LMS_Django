from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from .models import Attendance, Grade
from apps.classes.models import Enrollment
from datetime import date

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