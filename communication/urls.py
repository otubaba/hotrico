# from django.urls import path
# from . import views

# urlpatterns = [
#     path('message/<int:receiver_id>/', views.send_message, name='send_message'),
#     path('inbox/', views.inbox, name='inbox'),
# ]

from django.urls import path
from . import views

app_name = "communication"

urlpatterns = [

    path(
        'inbox/',
        views.inbox,
        name='inbox'
    ),


    path(
        'student/<int:student_id>/',
        views.message_student,
        name='message_student'
    ),

    path(
    'class/<int:classroom_id>/',
    views.message_class,
    name='message_class'
    ),
    
    path(
        'parent/<int:parent_id>/',
        views.message_parent,
        name='message_parent'
    ),
    path('compose/', views.compose, name='create_conversation'),
    path('notifications/', views.notifications, name='notifications'),
    path('chat/<int:conversation_id>/', views.chat_room, name='chat_room'),
]


