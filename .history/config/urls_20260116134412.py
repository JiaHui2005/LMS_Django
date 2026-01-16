from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from apps.accounts import views as account_views
from apps.classes.views import lecturer_classes
from apps.academics.views import take_attendance, enter_grade

def root_redirect(request):
    return redirect('/login/')

urlpatterns = [
    path('', root_redirect),
    path('admin/', admin.site.urls),

    # Auth
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),

    # Lecturer
    path('classes/lecturer/', lecturer_classes, name='lecturer_classes'),
    path('attendance/<int:class_id>/', take_attendance, name='attendance'),
    path('grade/<int:class_id>/', enter_grade, name='grade'),
    path('dashboard/manager/', account_views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/student/', account_views.student_dashboard, name='student_dashboard'),
    path('dashboard/lecturer/', account_views.lecturer_dashboard, name='lecturer_dashboard'),
    path('dashboard/cs/', account_views.cs_dashboard, name='cs_dashboard'),
    path('dashboard/coordinator/', account_views.coordinator_dashborad, name='coordinator_dashborad'),
    path('manager/users/', account_views.user_list, name='user_list'),
    path('manager/users/create/', account_views.user_create, name='user_create'),
    path('manager/users/<int:user_id>/edit/', account_views.user_edit, name='user_edit'),
    path('manager/users/<int:user_id>/delete/', account_views.user_delete, name='user_delete'),
]


