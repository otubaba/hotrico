
from django.core.exceptions import PermissionDenied

class TeacherRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'teacher':
            raise PermissionDenied("Only teachers allowed")
        return super().dispatch(request, *args, **kwargs)