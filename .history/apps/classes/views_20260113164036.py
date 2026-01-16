from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from common.decorators import role_required
from .models import Class

@login_required
@role_required('lecturer')
def lecturer_classes(request):
    classes = Class.objects.filter(lecturers=request.user)
    return render(request, 'classes/lecturer_classes.html', {
        'classes': classes
    })
