from django.urls import path
from . import views
from .views import StudentListView
urlpatterns = [

    path(
        'student/<int:student_id>/',
        views.student_detail,
        name='student_detail'
    ),

    path(
        '',
        StudentListView.as_view(),
        name='student_list'
    ),
]