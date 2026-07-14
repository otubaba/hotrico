
from django.db import models
from accounts.models import User
from academics.models import ClassRoom

from django.conf import settings
from datetime import datetime


import uuid

from django.db import models
from django.conf import settings


class Student(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)

    registration_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )
    
    classroom = models.ForeignKey(
        'academics.ClassRoom',
        on_delete=models.CASCADE
    )
    passport = models.ImageField(
        upload_to='passports/',
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
    null=True,
    blank=True
    )

    def save(self, *args, **kwargs):

        if not self.registration_number:
            self.registration_number = (
                f"SHD-{uuid.uuid4().hex[:6].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
