from django.db import models
from datetime import date
from django.conf import settings
# Create your models here.
# academics/models.py

class ClassRoom(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(
    'accounts.Teacher',
    on_delete=models.SET_NULL,
    null=True,
    blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

class AcademicSession(models.Model):
    name = models.CharField(max_length=20)  # e.g. 2025/2026
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# academics/models.py


from django.db import models
from django.utils import timezone


class Term(models.Model):

    SESSION_CHOICES = [
        ('2025/2026', '2025/2026'),
    ]

    TERM_CHOICES = [
        ('First Term', 'First Term'),
        ('Second Term', 'Second Term'),
        ('Third Term', 'Third Term'),
    ]

    session = models.CharField(
        max_length=20,
        choices=SESSION_CHOICES,
        default='2025/2026'
    )

    name = models.CharField(
        max_length=20,
        choices=TERM_CHOICES
    )

    registration_deadline = models.DateField()

    registration_open = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.session} - {self.name}"


class CourseRegistration(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    term = models.ForeignKey('Term', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'subject', 'term')

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.term})"
    def clean(self):
        if date.today() > self.term.registration_deadline:
            raise ValidationError("Registration period has closed.")


# class Result(models.Model):
#     registration = models.OneToOneField(
#         CourseRegistration,
#         on_delete=models.CASCADE
#     )

#     teacher = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

#     test = models.FloatField()
#     exam = models.FloatField()
#     remark = models.CharField(max_length=255, blank=True, null=True)

#     @property
#     def total(self):
#         return self.test + self.exam
    
#     def __str__(self):
#         return str(self.registration.id)

#     @property
#     def grade(self):
#         if self.total >= 70: return 'A'
#         elif self.total >= 60: return 'B'
#         elif self.total >= 50: return 'C'
#         elif self.total >= 45: return 'D'
#         elif self.total >= 40: return 'E'
#         return 'F'
# academics/models.py

from accounts.models import Teacher

class Result(models.Model):

    registration = models.ForeignKey(
        CourseRegistration,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
    Subject,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    test = models.FloatField(default=0)

    exam = models.FloatField(default=0)

    total = models.FloatField(
        default=0
    )

    grade = models.CharField(
        max_length=2,
        default='F',
        blank=True,
        null=True
    )

    remark = models.CharField(
        max_length=100,
        default='Pending',
        blank=True,
        null=True
    )

    teacher_comment = models.TextField(
        blank=True,
        null=True,
        default=''
    )

    def __str__(self):
        return f"{self.registration.student}"

    def save(self, *args, **kwargs):

        self.total = self.test + self.exam

        if self.total >= 70:
            self.grade = 'A'
            self.remark = 'Excellent'

        elif self.total >= 60:
            self.grade = 'B'
            self.remark = 'Very Good'

        elif self.total >= 50:
            self.grade = 'C'
            self.remark = 'Good'

        elif self.total >= 45:
            self.grade = 'D'
            self.remark = 'Pass'

        else:
            self.grade = 'F'
            self.remark = 'Fail'

        super().save(*args, **kwargs)


class ClassSubject(models.Model):
    classroom = models.ForeignKey('ClassRoom', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.classroom} - {self.subject}"
    

# academics/models.py

from django.core.exceptions import ValidationError

def clean(self):
    if self.teacher.role != 'teacher':
        raise ValidationError("Only teachers can assign results")






