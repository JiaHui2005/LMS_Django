import csv
import openpyxl
from django.shortcuts import render
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from common.decorators import role_required
from apps.classes.models import Class, Enrollment
from apps.accounts.models import User
from django.http import HttpResponse

# Create your views here.

# Index
@login_required
@role_required('manager')
def reports_index(request):
    return render(request, 'manager/reports/index.html')


# Bao cao lop hoc
@login_required
@role_required('manager')
def class_analysis(request):
    classes = (
        Class.objects
        .annotate(student_count=Count('enrollments'))
        .order_by('-student_count')
    )
    
    avg_student = classes.aggregate(avg=Avg('student_count'))['avg'] or 0
    
    most_class = classes.first()
    
    least_class = classes.last()
    
    context = {
        'classes': classes,
        'avg_student': avg_student,
        'most_class': most_class,
        'least_class': least_class,
    }
    
    return render(request, 'manager/reports/class_report.html', context)

# Bao cao giang vien
@login_required
@role_required('manager')
def lecturer_analysis(request):
    lecturers = (
        User.objects
        .filter(role='lecturer')
        .annotate(
            class_count = Count('teaching_classes', distinct=True),
            student_count = Count('teaching_classes__enrollments', distinct=True)
        ).order_by('-student_count')
    )
    
    top_lecturer = lecturers.first()
    lowest_lecturer = lecturers.last()
    
    total_students = Enrollment.objects.count()
    
    context = {
        'lecturers': lecturers,
        'top_lecturer': top_lecturer,
        'lowest_lecturer': lowest_lecturer,
        'total_students': total_students,
    }
    
    return render(request, 'manager/reports/lecturer_report.html', context)

# Bao cao theo thoi gian
@login_required
@role_required('manager')
def enrollment_trend(request):
    data = (
        Enrollment.objects
        .annotate(month=TruncMonth('joined_at'))
        .values('month')
        .annotate(total_count=Count('id'))
        .order_by('month')
    )
    
    max_val = max([item['total_count'] for item in data], default=0)
    
    context = {
        'data': data,
        'max_val': max_val
    }
    
    return render(request, 'manager/reports/time_report.html', context)

# Xuat bao cao
@login_required
@role_required('manager')
def export_class_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="class_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Lớp', 'Số học viên'])
    
    for c in Class.objects.annotate(student_count=Count('enrollment')):
        writer.writerow([c.name, c.student_count])
        
    return response

# Du lieu bieu do
@login_required
@role_required('manager')
def class_chart(request):
    classes = Class.objects.annotate(student_count=Count('enrollments'))
    
    labels = [c.name for c in classes]
    data = [c.student_count for c in classes]
    
    context = {
        'labels': labels,
        'data': data
    }
    
    return render(request, 'manager/reports/class_chart.html', context)

# Export Excel
@login_required
@role_required('manager')
def export_class_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Class Report"
    
    ws.append(['Tên lớp', 'Số học viên', 'Trạng thái'])
    
    classes = Class.objects.annotate(student_count=Count('enrollment'))
    
    for c in classes:
        ws.append([
            c.name,
            c.student_count,
            'Đang hoạt động' if c.is_active else 'Đã kết thúc'
        ])
        
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=class_report.xlsx'
    wb.save(response)
    
    return response
