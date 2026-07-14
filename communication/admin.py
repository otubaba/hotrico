from django.contrib import admin

from .models import (
    Conversation,
    Participant,
    Message,
    Attachment,
    Notification,
    MessageRead
)

admin.site.register(Conversation)
admin.site.register(Participant)
admin.site.register(Message)
admin.site.register(Attachment)
admin.site.register(Notification)
admin.site.register(MessageRead)