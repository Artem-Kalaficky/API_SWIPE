from rest_framework import permissions


class IsDeveloperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_developer


class IsMyContent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.house == obj.house


class IsMyRequest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.ad.house == request.user.house
