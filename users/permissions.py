from rest_framework.permissions import BasePermission


class UnauthorizedPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_anonymous)