from rest_framework.permissions import (
    BasePermission, SAFE_METHODS)


class UserPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class ModeratorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'Moderator':
            return True


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in SAFE_METHODS
            or obj.author == user or user.is_authenticated
            and user.is_admin or user.is_authenticated
            and user.is_moderator

        )
