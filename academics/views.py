from django.shortcuts import render, redirect
from communication.models import Message
# Create your views here.
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
from .models import Result, Term
from .utils import get_student_position, get_average, get_remark
from django.views.generic import CreateView
from django.urls import reverse_lazy
from accounts.mixins import TeacherRequiredMixin
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from .models import CourseRegistration, ClassSubject, Term

# academics/views.py

from django.http import HttpResponseForbidden
from .utils import is_registration_open



def student_results(request, student_id):
    results = Result.objects.filter(registration__student_id=student_id)
    return render(request, 'academics/student_results.html', {'results': results})


# academics/views.py
import os
import io
import qrcode
import matplotlib.pyplot as plt

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from students.models import Student
from .models import Result
from django.db.models import Sum
from reportlab.lib.utils import ImageReader

def get_position(pos):

    if 10 <= pos % 100 <= 20:
        suffix = "th"
    else:
        suffix = {
            1: "st",
            2: "nd",
            3: "rd"
        }.get(pos % 10, "th")

    return f"{pos}{suffix}"


from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
import os

def add_watermark(canvas, doc):

    logo_path = os.path.join(
        settings.MEDIA_ROOT,
        'school/logo.png'
    )

    if os.path.exists(logo_path):

        canvas.saveState()

        # Make watermark very light
        try:
            canvas.setFillAlpha(0.04)
        except:
            pass

        page_width, page_height = A4

        canvas.drawImage(
            ImageReader(logo_path),
            20,                # left margin
            50,                # bottom margin
            width=page_width-40,
            height=page_height-100,
            preserveAspectRatio=True,
            mask='auto'
        )

        canvas.restoreState()



def generate_report_card(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    results = Result.objects.filter(
        registration__student=student
    )

    # Calculate position in class

    class_students = Student.objects.filter(
        classroom=student.classroom
    )

    student_scores = []

    for s in class_students:

        total = Result.objects.filter(
            registration__student=s
        ).aggregate(
            total_score=Sum('total')
        )['total_score'] or 0

        student_scores.append({
            'student': s,
            'total': total
        })

    # Highest score first
    student_scores = sorted(
        student_scores,
        key=lambda x: x['total'],
        reverse=True
    )

    position = 1

    for index, item in enumerate(student_scores, start=1):

        if item['student'].id == student.id:
            position = index
            break

    position_text = get_position(position)

    total_score = sum(result.total for result in results)

    subject_count = results.count()

    average_score = round(
        total_score / subject_count,
        2
    ) if subject_count else 0

    if average_score >= 70:
        overall_grade = "A"

    elif average_score >= 60:
        overall_grade = "B"

    elif average_score >= 50:
        overall_grade = "C"

    elif average_score >= 45:
        overall_grade = "D"

    else:
        overall_grade = "F"
        
    response = HttpResponse(
            content_type='application/pdf'
        )

    response['Content-Disposition'] = (
        f'attachment; filename="report_card_{student.id}.pdf"'
    )

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
    buffer,
    pagesize=A4,
    topMargin=20,
    bottomMargin=20,
    leftMargin=20,
    rightMargin=20
    )

    elements = []

    styles = getSampleStyleSheet()

    # SCHOOL LOGO
    logo_path = os.path.join(
        settings.MEDIA_ROOT,
        'school/logo.png'
    )

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=80,
            height=80
        )

        

    # TITLE
    header_data = [[
    logo if os.path.exists(logo_path) else '',
    Paragraph(
        """
        <para align='center'>
        <font size='18'><b>SHIELDOEB COLLEGE</b></font><br/>
        KM 12 Ring Road, Hotoro, Kano State<br/>
        Tel: 080xxxxxxxx<br/>
        <b>STUDENT REPORT CARD</b>
        </para>
        """,
        styles['BodyText']
    )
    ]]

    header = Table(
        header_data,
        colWidths=[90, 420]
    )

    elements.append(header)
    elements.append(Spacer(1, 10))

    # STUDENT INFO
    passport_image = ''

    if student.passport:
        passport_image = Image(
            student.passport.path,
            width=80,
            height=80
        )

    student_info_table = Table([
    [
        Paragraph(
            f"""
            <b>Name:</b> {student.user.get_full_name()}<br/>
            <b>Reg No:</b> {student.registration_number}<br/>
            <b>Class:</b> {student.classroom}<br/>
            <b>Session:</b> 2025/2026<br/>
            <b>Term:</b> Third Term<br/>
            <b>Position:</b> {position_text}
            """,
            styles['BodyText']
        ),
        passport_image
    ]
    ], colWidths=[420, 100])

    student_info_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(student_info_table)
    elements.append(Spacer(1,10))


    # RESULTS TABLE
    data = [[
    'Subject',
    'CA',
    'Exam',
    'Total',
    'Grade',
    'Remark'
    ]]

    chart_subjects = []
    chart_scores = []

    for result in results:

        subject_name = (
            result.subject.name
            if result.subject
            else result.registration.subject.name
            if result.registration.subject
            else "No Subject"
        )

        data.append([
            subject_name,
            result.test,
            result.exam,
            result.total,
            result.grade,
            result.remark
        ])

        chart_subjects.append(subject_name)
        chart_scores.append(result.total)


    table = Table(
    data,
    colWidths=[120,50,50,50,50,120]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('BACKGROUND', (0, 1), (-1, -1), colors.white),

    ]))

    elements.append(table)
    elements.append(Spacer(1, 10))

    summary_data = [
    ['Total Subjects', subject_count],
    ['Total Score', total_score],
    ['Average Score', average_score],
    ['Overall Grade', overall_grade],
    ['Position', position_text],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[200,150]
    )

    summary_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1,10))

    #BEHAVIOUR TABLE

    behaviour = Table([
    ['Trait', 'Rating'],
    ['Punctuality', 'A'],
    ['Attendance', 'A'],
    ['Neatness', 'A'],
    ['Honesty', 'A'],
    ['Leadership', 'B']
    ])

    behaviour.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)
    ]))

    elements.append(behaviour)


    # QR CODE
    qr_data = (
        f"Student: {student.user.get_full_name()} "
        f"| ID: {student.id}"
    )

    qr = qrcode.make(qr_data)

    qr_path = os.path.join(
        settings.MEDIA_ROOT,
        f'qr_{student.id}.png'
    )

    qr.save(qr_path)

    qr_image = Image(
        qr_path,
        width=80,
        height=80
    )

    elements.append(Spacer(1, 20))

    # PRINCIPAL SIGNATURE
    elements.append(
    Paragraph(
        f"<b>Class Teacher's Remark:</b> Good performance. Keep improving.",
        styles['BodyText']
    )
    )

    elements.append(Spacer(1,5))

    elements.append(
        Paragraph(
            f"<b>Principal's Remark:</b> Promoted to the next class.",
            styles['BodyText']
        )
    )

    elements.append(Spacer(1,10))


    signature_table = Table([
    [
        qr_image,
        "__________________",
        "__________________"
    ],
    [
        "QR Verification",
        "Class Teacher",
        "Principal"
    ]
    ], colWidths=[120,180,180])

    elements.append(signature_table)


    footer = Paragraph(
    """
    <b>NOTE:</b>
    This report card is computer generated and
    authenticated with a QR code.
    """,
    styles['Italic']
    )

    elements.append(footer)

    # BUILD PDF
    doc.build(
    elements,
    onFirstPage=add_watermark,
    onLaterPages=add_watermark
    )

    pdf = buffer.getvalue()

    buffer.close()

    response.write(pdf)

    return response


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from students.models import Student


def download_report(request, student_id):

    # 1. Get the student properly using URL parameter
    student = get_object_or_404(Student, id=student_id)

    # 2. Fetch results through registration relationship
    results = Result.objects.filter(
        registration__student=student
    )

    # 3. Create response
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="report_{student.user.username}.txt"'

    # 4. Write report content
    response.write(f"REPORT CARD FOR: {student.user.get_full_name()}\n")
    response.write("=" * 40 + "\n\n")

    for r in results:
        subject = r.registration.subject.name if r.registration and r.registration.subject else "N/A"

        response.write(f"{subject}: {r.total} | Grade: {r.grade}\n")

    return response

# academics/views.py


from django.core.exceptions import PermissionDenied

from django.urls import reverse_lazy

class ResultCreateView(TeacherRequiredMixin, CreateView):
    model = Result
    fields = ['registration', 'test', 'exam']

    success_url = reverse_lazy('academics:result_list')

    def form_valid(self, form):

        registration = form.instance.registration
        student = registration.student

        teacher = self.request.user.teacher

        if student.classroom.teacher != teacher:
            raise PermissionDenied(
                "You cannot add results for this student"
            )

        form.instance.teacher = teacher
        form.instance.subject = registration.subject

        return super().form_valid(form)
    

from django.views.generic import UpdateView, DeleteView, ListView

# class ResultUpdateView(TeacherRequiredMixin, UpdateView):
#     model = Result
#     fields = ['test', 'exam']
#     template_name = 'academics/result_form.html'
#     success_url = reverse_lazy('teacher_dashboard')

#     def get_queryset(self):
#         return Result.objects.filter(teacher=self.request.user)


class ResultUpdateView(TeacherRequiredMixin, UpdateView):

    model = Result
    fields = ['test', 'exam']
    template_name = 'academics/result_form.html'

    def get_queryset(self):

        return Result.objects.filter(
            teacher=self.request.user.teacher
        )

    def get_success_url(self):

        return reverse_lazy('result_list')
    


def dispatch(self, request, *args, **kwargs):
    if request.method in ['POST', 'PUT', 'DELETE']:
        if request.user.role != 'teacher':
            return HttpResponse("Forbidden", status=403)
    return super().dispatch(request, *args, **kwargs)



# class ResultListView(TeacherRequiredMixin, ListView):
#     model = Result
#     template_name = 'academics/result_list.html'

#     def get_queryset(self):
#         return Result.objects.filter(teacher=self.request.user)
    

class ResultListView(ListView):

    model = Result
    template_name = 'academics/result_list.html'
    context_object_name = 'results'

    def get_queryset(self):

        return Result.objects.filter(
            teacher=self.request.user.teacher
        )


from django.urls import reverse_lazy
from django.views.generic import DeleteView


class ResultDeleteView(DeleteView):

    model = Result
    template_name = 'academics/result_confirm_delete.html'
    success_url = reverse_lazy('academics:result_list')

    def get_queryset(self):

        return Result.objects.filter(
            teacher=self.request.user.teacher
        )
    
# academics/views.py


def register_courses(request):
    student = request.user.student
    term = Term.objects.last()

    # 🔒 BLOCK IF DEADLINE PASSED
    if not is_registration_open(term):
        return HttpResponseForbidden(
            "Course registration is closed for this term."
        )

    subjects = ClassSubject.objects.filter(
    classroom=student.classroom)

    if request.method == 'POST':
        selected_subjects = request.POST.getlist('subjects')

        CourseRegistration.objects.filter(
            student=student,
            term=term
        ).delete()

        for subject_id in selected_subjects:
            CourseRegistration.objects.create(
                student=student,
                subject_id=subject_id,
                term=term
            )

        return redirect('student_dashboard')

    return render(request, 'academics/register_courses.html', {
        'subjects': subjects,
        'term': term,
        'is_open': is_registration_open(term)
    })

# academics/views.py

from .forms import ResultForm
from django.shortcuts import get_object_or_404

def add_result(request, registration_id):

    registration = get_object_or_404(
        CourseRegistration,
        id=registration_id
    )

    result, created = Result.objects.get_or_create(
        registration=registration,
        defaults={
            'teacher': request.user.teacher
            
        }
    )

    if request.method == 'POST':

        form = ResultForm(request.POST, instance=result)

        if form.is_valid():

            form.save()

            return redirect(
                'student_detail',
                student_id=registration.student.id
            )

    else:

        form = ResultForm(instance=result)

    return render(
        request,
        'academics/add_result.html',
        {
            'form': form,
            'registration': registration
        }
    )


def form_valid(self, form):
    registration = form.instance.registration

    if registration.student.class_name != registration.subject:
        pass  # optional extra validation

    form.instance.teacher = self.request.user
    return super().form_valid(form)




from accounts.models import Parent




def student_detail_for_teacher(request, student_id):

    student = get_object_or_404(
        Student.objects.select_related(
            'user',
            'classroom'
        ),
        pk=student_id
    )

    term = Term.objects.last()

    registrations = CourseRegistration.objects.filter(
        student=student,
        term=term
    ).select_related('subject')

    # Parent linked to this student
    parent = Parent.objects.filter(
        children__id=student.id
    ).select_related('user').first()

    # Class teacher
    teacher = getattr(student.classroom, 'teacher', None)

    context = {
        'student': student,
        'parent': parent,
        'teacher': teacher,
        'registrations': registrations,
        'term': term,
    }

    return render(
        request,
        'dashboard/student_detail.html',
        context
    )

