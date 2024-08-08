from rest_framework.permissions import BasePermission

class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.otp_verified
