from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.sender} -> {self.receiver}"
    

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):

    PRIVATE = "private"
    GROUP = "group"
    CLASS = "class"

    TYPES = (
        (PRIVATE, "Private"),
        (GROUP, "Group"),
        (CLASS, "Class"),
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    conversation_type = models.CharField(
        max_length=20,
        choices=TYPES,
        default=PRIVATE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title or f"Conversation {self.id}"
    

class Participant(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='participants'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('conversation', 'user')


class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_at']

class Attachment(models.Model):

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='attachments'
    )

    file = models.FileField(
        upload_to='communication/files/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )



class MessageRead(models.Model):

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    read_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('message', 'user')



class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title

