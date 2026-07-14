from django.contrib import admin
from .models import Result
from django.db import models
from .models import AcademicSession

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = (
        'get_student',
        'get_subject',
        'test',
        'exam',
        'total',
    )

    list_filter = (
        'registration__subject',
    )

    def get_student(self, obj):
        return obj.registration.student

    get_student.short_description = 'Student'

    def get_subject(self, obj):
        return obj.registration.subject

    get_subject.short_description = 'Subject'


from django.contrib import admin

from .models import (
    ClassRoom,
    Subject,
    Term,
    ClassSubject,
    CourseRegistration,
    Enrollment
)


admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Term)
admin.site.register(ClassSubject)
admin.site.register(CourseRegistration)
admin.site.register(Enrollment)

admin.site.register(AcademicSession)
# @admin.register(Result)
# class ResultAdmin(admin.ModelAdmin):

#     list_display = (
#         'registration',
#         'teacher',
#         'test',
#         'exam',
#         'total',
#     )

#     list_filter = (
#         'teacher',
#     )