# from django.shortcuts import render
# from django.http import HttpResponse
# # Create your views here.
from django.shortcuts import render, redirect
# from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()
from students.models import Student
from accounts.models import Parent
from .models import Conversation, Participant, Notification


from django.shortcuts import get_object_or_404, redirect
from students.models import Student
from .models import Conversation, Participant, Message


from django.contrib.auth.decorators import login_required




@login_required
def inbox(request):

    conversations = Conversation.objects.filter(
        participants__user=request.user
    ).distinct()

    return render(
        request,
        'communication/inbox.html',
        {
            'conversations': conversations
        }
    )


def chat_room(request, conversation_id):

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id
    )

    messages = conversation.messages.select_related(
        'sender'
    )

    if request.method == "POST":

        content = request.POST.get("content")

        if content:

            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

        return redirect(
            'communication:chat_room',
            conversation_id=conversation.id
        )

    return render(
        request,
        'communication/chat_room.html',
        {
            'conversation': conversation,
            'messages': messages
        }
    )



def message_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    teacher_user = request.user
    student_user = student.user

    # Look for existing private conversation
    conversation = None

    conversations = Conversation.objects.filter(
        conversation_type='private'
    )

    for conv in conversations:

        participants = list(
            conv.participants.values_list(
                'user_id',
                flat=True
            )
        )

        if set(participants) == {
            teacher_user.id,
            student_user.id
        }:
            conversation = conv
            break

    # Create one if it doesn't exist
    if not conversation:

        conversation = Conversation.objects.create(
            conversation_type='private',
            title=f"{teacher_user.username} - {student_user.username}"
        )

        Participant.objects.create(
            conversation=conversation,
            user=teacher_user
        )

        Participant.objects.create(
            conversation=conversation,
            user=student_user
        )

    return redirect(
        'communication:chat_room',
        conversation_id=conversation.id
    )


from students.models import Student
from academics.models import ClassRoom


@login_required
def message_class(request, classroom_id):

    classroom = get_object_or_404(
        ClassRoom,
        id=classroom_id
    )

    conversation, created = Conversation.objects.get_or_create(
        title=f"{classroom.name} Class Group",
        conversation_type=Conversation.CLASS
    )

    # Add teacher
    Participant.objects.get_or_create(
        conversation=conversation,
        user=request.user
    )

    # Add all students
    students = Student.objects.filter(
        classroom=classroom
    ).select_related('user')

    for student in students:
        Participant.objects.get_or_create(
            conversation=conversation,
            user=student.user
        )

    if request.method == "POST":

        content = request.POST.get("content")

        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )

        return redirect(
            'communication:chat_room',
            conversation_id=conversation.id
        )

    return render(
        request,
        'communication/message_class.html',
        {
            'classroom': classroom,
            'conversation': conversation,
            'students': students
        }
    )



@login_required
def message_parent(request, parent_id):

    parent = get_object_or_404(
        Parent,
        id=parent_id
    )

    conversation = None

    conversations = Conversation.objects.filter(
        conversation_type=Conversation.PRIVATE
    )

    for conv in conversations:

        users = set(
            conv.participants.values_list(
                'user_id',
                flat=True
            )
        )

        if users == {request.user.id, parent.user.id}:
            conversation = conv
            break

    if not conversation:

        conversation = Conversation.objects.create(
            conversation_type=Conversation.PRIVATE
        )

        Participant.objects.create(
            conversation=conversation,
            user=request.user
        )

        Participant.objects.create(
            conversation=conversation,
            user=parent.user
        )

    return redirect(
        'communication:chat_room',
        conversation_id=conversation.id
    )


# communication/views.py

@login_required
def notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'communication/notifications.html',
        {'notifications': notifications}
    )


@login_required
def compose(request):
    users = User.objects.exclude(
        id=request.user.id
    )

    return render(
        request,
        'communication/compose.html',
        {'users': users}
    )



