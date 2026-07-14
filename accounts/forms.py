from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from students.models import Student
from academics.models import ClassRoom




class StudentRegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'First Name'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Last Name'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Email Address'
        })
    )

    passport = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full p-3 border rounded-lg bg-white'
        })
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    classroom = forms.ModelChoiceField(
        queryset=ClassRoom.objects.all(),
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:

        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


    def save(self, commit=True):

        user = super().save(commit=False)

        # USER DETAILS
        user.first_name = self.cleaned_data.get('first_name')

        user.last_name = self.cleaned_data.get('last_name')

        user.email = self.cleaned_data.get('email')

        user.role = 'student'

        if commit:

            user.save()

            # AUTO GENERATE REGISTRATION NUMBER
            last_student = Student.objects.order_by('-id').first()

            if last_student and last_student.registration_number:

                try:
                    last_number = int(
                        last_student.registration_number.split('-')[-1]
                    )

                except:
                    last_number = 0

            else:
                last_number = 0

            new_number = last_number + 1

            registration_number = f"STD-{new_number:04d}"

            # CREATE STUDENT PROFILE
            Student.objects.create(

                user=user,

                classroom=self.cleaned_data.get('classroom'),

                passport=self.cleaned_data.get('passport'),

                date_of_birth=self.cleaned_data.get('date_of_birth'),

                registration_number=registration_number

            )

        return user