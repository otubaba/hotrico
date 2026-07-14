from django.urls import path
from .views import TeacherDashboardView, AdminDashboardView, StudentDashboardView
from . import views
urlpatterns = [
    path('teacher-dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('student-dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path(
    'parent-dashboard/',
    views.ParentDashboardView.as_view(),
    name='parent_dashboard'
),
]
# dashboard/urls.py

