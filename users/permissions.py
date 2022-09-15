from rest_framework import permissions


class IsMyFilter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsMyProfile(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser is False and request.user.is_staff is False \
               and request.user.is_developer is False
