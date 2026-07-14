from django.shortcuts import render, redirect
# Create your views here.
from django.db import models
from django.views.generic import TemplateView
from academics.models import ClassRoom, Result, Term, ClassSubject
from students.models import Student
from academics.utils import is_registration_open
from django.http import HttpResponseForbidden
from academics.models import CourseRegistration

from communication.models import Message
from django.views.generic import TemplateView
from students.models import Student


from django.views.generic import TemplateView
from students.models import Student
from academics.models import ClassRoom


class TeacherDashboardView(TemplateView):
    template_name = "dashboard/teacher.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = self.request.user.teacher

        classrooms = ClassRoom.objects.filter(
            teacher=teacher
        )

        students = Student.objects.filter(
            classroom__teacher=teacher
        ).select_related(
            'user',
            'classroom'
        )

        context.update({
            'teacher': teacher,
            'classrooms': classrooms,
            'students': students,
            'student_count': students.count(),
        })

        return context


def dashboard_redirect(request):

    if request.user.role == 'student':
        return redirect('student_dashboard')

    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')

    elif request.user.role == 'parent':
        return redirect('parent_dashboard')

    elif request.user.role == 'head_teacher':
        return redirect('head_teacher_dashboard')

    return redirect('login')
# dashboard/views.py



class AdminDashboardView(TemplateView):
    template_name = 'dashboard/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_students'] = Student.objects.count()
        context['total_classes'] = ClassRoom.objects.count()
        context['results'] = Result.objects.all()[:5]
        

        return context

# dashboard/views.py
class TeacherStudentsView(TemplateView):
    template_name = 'dashboard/teacher_students.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teacher = self.request.user.teacher

        context['students'] = Student.objects.filter(
            classroom__teacher=teacher
        )

        return context

# dashboard/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from communication.models import Message

from accounts.models import Parent

class StudentDashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/student.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        student = Student.objects.select_related(
            'user',
            'classroom'
        ).filter(
            user=self.request.user
        ).first()

        if not student:
            context['error'] = "Student profile not found."
            return context

        registrations = CourseRegistration.objects.filter(
            student=student
        ).select_related(
            'subject',
            'term'
        )

        results = Result.objects.filter(
            registration__student=student
        ).select_related(
            'registration',
            'subject',
            'teacher'
        )

        recent_messages = Message.objects.filter(
            conversation__participants__user=self.request.user
        ).exclude(
            sender=self.request.user
        ).select_related(
            'sender',
            'conversation'
        ).order_by('-created_at')[:5]

        messages = Message.objects.filter(
            conversation__participants__user=self.request.user
        ).distinct()

        # Parent
        parent = Parent.objects.filter(
            children=student
        ).select_related(
            'user'
        ).first()

        # Teacher (adjust if your ClassRoom model uses a different field name)
        teacher = getattr(student.classroom, 'teacher', None)

        context.update({
            'student': student,
            'parent': parent,
            'teacher': teacher,
            'registrations': registrations,
            'results': results,
            'recent_messages': recent_messages,
            'messages': messages,
            'message_count': messages.count(),
        })

        return context


from django.contrib.auth.mixins import LoginRequiredMixin

class ParentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/parent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parent = self.request.user.parent
        context['children'] = parent.children.all()

        return context




def student_dashboard(request):
    student = request.user.student
    term = Term.objects.last()

    context = {
        'registration_open': is_registration_open(term),
        'deadline': term.registration_deadline
    }

    return render(request, 'dashboard/student.html', context)
