from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role == "teacher":
            return True
        else:
            return False