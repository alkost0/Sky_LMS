from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором!"

    def has_permission(self, request, view):
        if request.user.role == UserRoles.moderator:
            return True
        return False


class IsBuyer(BasePermission):
    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        if obj.buyer == request.user or request.user.is_superuser:
            return True
        return False
