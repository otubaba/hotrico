from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )



class Teacher(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher'
    )

    qualification = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.get_full_name()


class Parent(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='parent'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    occupation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    children = models.ManyToManyField(
        'students.Student',
        blank=True
    )

    def __str__(self):

        return self.user.get_full_name()