# academics/utils.py

from django.db.models import Sum
from .models import Result
from django.db.models import Avg

def get_student_position(student, term):
    students = (
        Result.objects
        .filter(term=term)
        .values('student')
        .annotate(total_score=Sum('test') + Sum('exam'))
        .order_by('-total_score')
    )

    for index, s in enumerate(students, start=1):
        if s['student'] == student.id:
            return index

    return None

# academics/utils.py

def get_remark(avg_score):
    if avg_score >= 70:
        return "Excellent performance"
    elif avg_score >= 60:
        return "Very good"
    elif avg_score >= 50:
        return "Good"
    elif avg_score >= 40:
        return "Fair"
    return "Needs improvement"



def get_average(student, term):
    return Result.objects.filter(student=student, term=term).aggregate(
        avg=Avg('test') + Avg('exam')
    )['avg'] or 0


# academics/utils.py

from datetime import date


# academics/utils.py

def is_teacher_of_student(teacher, student):
    return student.classroom.teacher == teacher.teacher


from django.utils import timezone


def is_registration_open(term):

    if not term:
        return False

    today = timezone.now().date()

    return today <= term.registration_deadline