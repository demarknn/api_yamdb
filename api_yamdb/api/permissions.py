from rest_framework.permissions import (
    BasePermission, SAFE_METHODS)


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True


class ModeratorPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'moderator':
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
