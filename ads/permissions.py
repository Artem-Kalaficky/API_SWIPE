from rest_framework import permissions


class IsMyAd(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj in request.user.ad.all()


class IsMyPromotion(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.ad in request.user.ad.all()
