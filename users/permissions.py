from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner or request.user.is_superuser:
            return True


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.user.is_superuser:
            return True


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
