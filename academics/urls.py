from django.urls import path
from . import views

from django.urls import path
from .views import ResultCreateView, ResultListView, ResultUpdateView, ResultDeleteView, generate_report_card

app_name = 'academics'

urlpatterns = [
    path('results/<int:student_id>/', views.student_results, name='student_results'),
    path('report/<int:student_id>/', views.generate_report_card, name='report_card'),
    path('report/<int:student_id>/', generate_report_card, name='download_report'),
    # path('download-report/<int:student_id>/', views.download_report, name='download_report'),
    path('register-courses/', views.register_courses, name='register_courses'),
    path('student/<int:student_id>/', views.student_detail_for_teacher, name='student_detail'),

    path('add-result/<int:registration_id>/', views.add_result, name='add_result'),
    path('results/', ResultListView.as_view(), name='result_list'),
    path('results/add/', ResultCreateView.as_view(), name='result_add'),
    path('results/<int:pk>/edit/', ResultUpdateView.as_view(), name='result_edit'),
    path('results/<int:pk>/delete/', ResultDeleteView.as_view(), name='result_delete'),
    ]
