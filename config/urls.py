from django.urls import path
from django.contrib import admin
from django.shortcuts import redirect
from apps.classes import views as class_views
from apps.reports import views as report_views
from apps.accounts import views as account_views
from apps.schedules import views as schedule_views
from apps.academics import views as academic_views
from apps.notifications import views as notification_views
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
    path('classes/lecturer/', class_views.lecturer_classes, name='lecturer_classes'),
    path('attendance/<int:class_id>/', take_attendance, name='attendance'),
    path('grade/<int:class_id>/', enter_grade, name='grade'),
    
    # Dashboard
    path('dashboard/manager/', account_views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/student/', account_views.student_dashboard, name='student_dashboard'),
    path('dashboard/lecturer/', account_views.lecturer_dashboard, name='lecturer_dashboard'),
    path('dashboard/cs/', account_views.cs_dashboard, name='cs_dashboard'),
    path('dashboard/coordinator/', account_views.coordinator_dashboard, name='coordinator_dashboard'),
    
    # CRUD User
    path('manager/users/', account_views.user_list, name='user_list'),
    path('manager/users/create/', account_views.user_create, name='user_create'),
    path('manager/users/<int:user_id>/edit/', account_views.user_edit, name='user_edit'),
    path('manager/users/<int:user_id>/delete/', account_views.user_delete, name='user_delete'),
    
    #CRUD Class & Schedules
    path('manager/classes', class_views.class_list, name='class_list'),
    path('manager/classes/create/', class_views.class_create, name='class_create'),
    path('manager/classes/<int:class_id>/schedules/', schedule_views.class_schedule_list, name='class_schedule_list'),
    path('manager/classes/<int:class_id>/schedules/create/', schedule_views.class_schedule_create, name='class_schedule_create'),
    path('manager/classes/<int:class_id>/schedules/<int:schedule_id>/edit/', schedule_views.class_schedule_edit, name='class_schedule_edit'),
    path('manager/classes/<int:class_id>/edit/', class_views.class_edit, name='class_edit'),
    path('manager/schedules/<int:schedule_id>/status/', schedule_views.schedule_update_status, name='schedule_update_status'),
    path('manager/classes/<int:class_id>/schedules/bulk-create/', schedule_views.class_schedule_bulk_create, name='class_schedule_bulk_create'),
    path('manager/classes/<int:class_id>/deactivate/', class_views.class_deactivate, name='class_deactivate'),
    path('manager/classes/<int:class_id>/schedules/<int:schedule_id>/makeup/', schedule_views.class_schedule_makeup, name='class_schedule_makeup'),
    path('manager/classes/<int:class_id>/schedules/<int:schedule_id>/delete/', schedule_views.class_schedule_delete, name='class_schedule_delete'),

    
    # CRUD Notification
    path('manager/notifications', notification_views.notification_list, name='notification_list'),
    path('manager/notifications/create/', notification_views.notification_create, name='notification_create'),
    path('manager/notifications/<int:notification_id>/edit/', notification_views.notification_edit, name='notification_edit'),
    path('manager/notifications/<int:notification_id>/toggle/', notification_views.notification_toggle, name='notification_toggle'),
    
    # Manager Report
    path('manager/reports', report_views.reports_index, name='reports_index'),
    path('manager/reports/classes/', report_views.class_analysis, name='class_analysis'),
    path('manager/reports/lecturers/', report_views.lecturer_analysis, name='lecturer_analysis'),
    path('manager/reports/enrollments/', report_views.enrollment_trend, name='enrollment_trend'),
    path('manager/reports/classes/export/csv', report_views.export_class_report, name='export_class_report'),
    path('manager/reports/classes/chart/', report_views.class_chart, name='class_chart'),
    path('manager/reports/classes/export/excel', report_views.export_class_excel, name='export_class_excel'),
    
    # Student
    path('student/classes/', academic_views.my_classes, name='student_my_classes'),
    path('student/schedule/', schedule_views.student_schedule_calendar, name='student_schedule'),
    path('student/classes/<int:class_id>/', academic_views.class_detail, name='student_class_detail'),
    path('student/enroll/', class_views.enroll_list, name='student_enroll'),
    path('student/enroll/<int:class_id>/', class_views.enroll_class, name='student_enroll_class'),
    path('student/notifications/', notification_views.student_notification_list, name='student_notifications'),
    path('student/notifications/<int:notification_id>/read/', notification_views.make_notification_read, name='mark_notification_read'),

]


