from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from common.decorators import role_required
from .forms import NotificationForm
from .models import Notification

# Create your views here.

# Lay danh sach thong bao
@login_required
@role_required('manager')
def notification_list(request):
    notifications = Notification.objects.all().order_by('-created_at')
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'manager/notification_list.html', context)

# Tao thong bao
@login_required
@role_required('manager')
def notification_create(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        
        if form.is_valid():
            notification = form.save(commit=True)
            notification.created_by = request.user
            notification.save()
            
            messages.success(
                request,
                'Tạo thông báo thành công.'
            )    
            return redirect('notification_list')
    else:
        form = NotificationForm()
        
    context = {
        'form': form,
        'title': 'Tạo thông báo', 
    }
    
    return render(request, 'manager/notification_form.html', context)

# Chinh sua thong bao
@login_required
@role_required('manager')
def notification_edit(request, notification_id):
    notifcation = get_object_or_404(Notification, id=notification_id)
    
    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notifcation)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Chỉnh sửa thông báo thành công.'
            )
            return redirect('notification_list')
    else:
        form = NotificationForm(instance=notifcation)
    
    context = {
        'form': form,
        'title': 'Chỉnh sửa thông báo.'
    }
    
    return render(request, 'manager/notification_form.html', context)

# Tat thong bao
@login_required
@role_required('manager')
def notification_toggle(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_active = not notification.is_active
    notification.save()
    
    messages.info(
        request,
        'Đã cập nhật trạng thái thông báo.'
    )
    
    return redirect('notification_list')
     
   
            
        
        
            
    
