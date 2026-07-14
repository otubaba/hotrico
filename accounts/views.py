from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import StudentRegistrationForm


from django.contrib import messages
from django.shortcuts import render, redirect

def register_view(request):

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            # prevent login
            messages.success(
                request,
                "Registration successful. Wait for admission approval."
            )

            return redirect('login')

    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })

# def register_view(request):

#     if request.method == 'POST':

#         form = StudentRegistrationForm(
#             request.POST,
#             request.FILES
#         )

#         if form.is_valid():

#             user = form.save()

#             login(request, user)

#             return redirect('student_dashboard')

#     else:

#         form = StudentRegistrationForm()

#     return render(
#         request,
#         'accounts/register.html',
#         {'form': form}
#     )


# from django.contrib.auth import get_user_model

# User = get_user_model()


# def register_view(request):

#     if request.method == 'POST':

#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # CHECK USERNAME
#         if User.objects.filter(username=username).exists():

#             messages.error(
#                 request,
#                 'Username already exists'
#             )

#             return redirect('register')

#         # CHECK EMAIL
#         if User.objects.filter(email=email).exists():

#             messages.error(
#                 request,
#                 'Email already registered'
#             )

#             return redirect('register')

#         # CREATE USER
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         # ASSIGN ROLE
#         user.role = 'student'

#         # ACCOUNT AWAITS APPROVAL
#         user.is_active = False

#         user.save()

#         messages.success(
#             request,
#             'Registration successful. Wait for admission approval.'
#         )

#         return redirect('login')

#     return render(
#         request,
#         'accounts/register.html'
#     )



def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # STUDENT APPROVAL CHECK
            if user.role == 'student':

                # check if student profile exists
                if hasattr(user, 'student'):

                    # block unapproved students
                    if not user.student.approved:

                        messages.error(
                            request,
                            'Your admission is still pending approval.'
                        )

                        return redirect('login')

            # LOGIN USER
            login(request, user)

            # ADMIN
            if user.role == 'admin':
                return redirect('admin_dashboard')

            # TEACHER
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')

            # STUDENT
            elif user.role == 'student':
                return redirect('student_dashboard')

            # PARENT
            elif user.role == 'parent':
                return redirect('parent_dashboard')

            # DEFAULT FALLBACK
            else:
                return redirect('home')

        else:

            messages.error(
                request,
                'Invalid username or password'
            )

            return redirect('login')

    return render(request, 'accounts/login.html')

# from django.contrib.auth import authenticate, login
# from django.contrib import messages

# def user_login(request):

#     if request.method == 'POST':

#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         if user is not None:

#             # check approval
#             if hasattr(user, 'student'):

#                 if not user.student.approved:

#                     messages.error(
#                         request,
#                         "Your admission is still pending approval."
#                     )

#                     return redirect('login')

#             login(request, user)

#             return redirect('dashboard')

#         else:
#             messages.error(request, 'Invalid credentials')

#     return render(request, 'accounts/login.html')



def logout_view(request):

    logout(request)

    return redirect('login')