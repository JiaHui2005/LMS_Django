from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from apps.accounts.views import login_view
from apps.classes.views import lecturer_classes
from apps.academics.views import take_attendance, enter_grade

def root_redirect(request):
    return redirect('/login/')

urlpatterns = [
    path('', root_redirect)
    path('admin/', admin.site.urls),

    # Auth
    path('login/', login_view, name='login'),

    # Lecturer
    path('classes/lecturer/', lecturer_classes, name='lecturer_classes'),
    path('attendance/<int:class_id>/', take_attendance, name='attendance'),
    path('grade/<int:class_id>/', enter_grade, name='grade'),
]
