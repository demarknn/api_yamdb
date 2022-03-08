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


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True


class ModeratorPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True


class MeUserPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user or request.user.is_authenticated
        )


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class AdminModeratorAuthorPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
