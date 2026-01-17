from django.shortcuts import render, get_object_or_404, redirect
from apps.classes.models import Enrollment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from apps.classes.models import Class
from .models import ClassSchedule
from .forms import ClassScheduleForm, MakeupScheduleForm, ScheduleStatusForm, BulkScheduleForm
from datetime import timedelta

# Create your views here.

# Thoi khoa bieu
@login_required
@role_required('student')
def student_schedule(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    
    context = {
        'enrollments': enrollments
    }
    
    return render(request, 'student/schedule.html', context)

# Danh sach lich hoc cua mot lop
@login_required
@role_required('manager')
def class_schedule_list(request, class_id):
    classroom = get_object_or_404(Class, id=class_id)
    schedules = classroom.schedules.all()
    
    context = {
        'classroom': classroom,
        'schedules': schedules
    }
    
    return render(request, 'manager/schedules/list.html', context)

# Them lich hoc
@login_required
@role_required('manager')
def class_schedule_create(request, class_id):
    classroom = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        form = ClassScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.classroom = classroom
            schedule.save()
            return redirect('class_schedule_list', class_id=class_id)
    else:
        form = ClassScheduleForm()

    return render(request, 'manager/schedules/form.html', {
        'form': form,
        'classroom': classroom
    })

# Thay doi trang thai buoi hoc
@login_required
@role_required(['lecturer', 'manager'])
def update_schedule_status(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)

    if request.method == 'POST':
        form = ScheduleStatusForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('class_schedule_list', class_id=schedule.classroom.id)
    else:
        form = ScheduleStatusForm(instance=schedule)

    return render(request, 'manager/schedules/status_form.html', {
        'form': form,
        'schedule': schedule
    })

# Tao nhieu buoi hoc
@login_required
@role_required('manager')
def class_schedule_bulk_create(request, class_id):
    classroom = get_object_or_404(Class, id=class_id)
    
    if request.method == 'POST':
        form = BulkScheduleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            current_date = data['start_date']
            created = 0
            
            while created < data['total_sessions']:
                if current_date.weekday() == int(data['day_of_week']):
                    ClassSchedule.objects.create(
                        classroom=classroom,
                        day_of_week=data['day_of_week'],
                        start_time=data['start_time'],
                        end_time=data['end_time'],
                        room=data['room'],
                        date=current_date
                    )
                    created += 1

                current_date += timedelta(days=1)
            messages.success(
                request,
                f'Đã tạo {created} buổi học.'
            )
            return redirect('class_schedule_list', class_is=classroom.id)
    else:
        form = BulkScheduleForm()
            
    context = {
        'form': form,
        'classroom': classroom
    }
    
    return render(request, 'manager/schedules/bulk_form.html', context)

# Sua lich hoc
@login_required
@role_required('manager')
def class_schedule_edit(request, class_id, schedule_id):
    classroom = get_object_or_404(Class, id=class_id)
    schedule = get_object_or_404(ClassSchedule, id=schedule_id, classroom=classroom)
    
    if request.method == 'POST':
        form = ClassScheduleForm(request.POST, instance=schedule)
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Chỉnh sửa lịch học thành công'
            )
            return redirect('class_schedule_list', class_id=classroom.id)
    else:
        form = ClassScheduleForm(instance=schedule)
        
    context = {
        'form': form,
        'classroom': classroom,
        'schedule': schedule,
        'title': 'Chỉnh sửa lịch học'
    }
    
    return render(request, 'manager/schedules/form.html', context)
        
# Xoa buoi hoc
@login_required
@role_required('manager')
def class_schedule_delete(request, class_id, schedule_id):
    classroom = get_object_or_404(Class, id=class_id)
    schedule = get_object_or_404(ClassSchedule, id=schedule_id, classroom=classroom)
    schedule.delete()
    
    messages.success(
        request,
        'Xóa lịch học thành công'
    )
    
    return redirect('class_schedule_list', class_id=classroom.id)

# Bao vang
@login_required
@role_required('manager')
def schedule_update_status(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)

    # Đổi trạng thái sang "giảng viên vắng"
    schedule.status = 'cancelled'
    schedule.save()

    messages.warning(
        request,
        f'Buổi học ngày {schedule.date} đã được đánh dấu là giảng viên vắng.'
    )

    return redirect('class_schedule_list', schedule.classroom.id)

# Tao buoi bu
@login_required
@role_required('manager')
def class_schedule_makeup(request, class_id, schedule_id):
    classroom = get_object_or_404(Class, id=class_id)

    original = get_object_or_404(
        ClassSchedule,
        id=schedule_id,
        classroom=classroom,
        status='cancelled'
    )

    if request.method == 'POST':
        form = MakeupScheduleForm(request.POST)
        if form.is_valid():
            makeup = form.save(commit=False)

            # Kế thừa thông tin từ buổi bị hủy
            makeup.classroom = classroom
            makeup.day_of_week = makeup.date.weekday()
            makeup.status = 'makeup'

            makeup.save()

            messages.success(
                request,
                'Đã tạo buổi học bù thành công.'
            )

            return redirect('class_schedule_list', class_id=classroom.id)
    else:
        # Gợi ý dữ liệu ban đầu từ buổi bị hủy
        form = MakeupScheduleForm(initial={
            'start_time': original.start_time,
            'end_time': original.end_time,
            'room': original.room,
        })

    context = {
        'form': form,
        'classroom': classroom,
        'original': original
    }

    return render(request, 'manager/schedules/makeup_form.html', context)
