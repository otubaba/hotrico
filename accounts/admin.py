from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User, Teacher, Parent


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
    )

    list_filter = (
        'role',
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'qualification',
        'phone',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
    )



@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'phone',
        'occupation',
    )

    filter_horizontal = (
        'children',
    )
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
    )