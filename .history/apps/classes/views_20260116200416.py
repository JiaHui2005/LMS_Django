from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from common.decorators import role_required
from .models import Class
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
