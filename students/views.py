from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from students.models import Student
from academics.models import CourseRegistration


def student_detail(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    registrations = CourseRegistration.objects.filter(
        student=student
    )

    return render(
        request,
        'dashboard/student_detail.html',
        {
            'student': student,
            'registrations': registrations
        }
    )


from django.views.generic import ListView
from .models import Student


class StudentListView(ListView):

    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

