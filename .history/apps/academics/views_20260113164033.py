from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from .models import Attendance
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
