from django.shortcuts import render, redirect, get_object_or_404
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
        form = ClassForm(instance=class_obj)
        
    context = {
        'form': form,
        'title': 'Chỉnh sửa lớp học.'
    }
    
    return redirect(request, 'manager/class_form.html', context)

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
