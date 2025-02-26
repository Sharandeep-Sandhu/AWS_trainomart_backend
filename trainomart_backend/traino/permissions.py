from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    """
    Custom permission to allow only students to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsInstructor(permissions.BasePermission):
    """
    Custom permission to allow only instructors to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.role == 'instructor'

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow only admins to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'
