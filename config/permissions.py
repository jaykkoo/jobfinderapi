from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.professional == request.user

class IsProfessional(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.is_professional
