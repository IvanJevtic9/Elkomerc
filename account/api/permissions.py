from rest_framework import permissions
from rest_framework import authentication

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class AnonPermissionOnly(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message = 'You are already authenticated, please log out.'

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    message = 'You do not have permissions for this request.'

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'email_id'):
            return obj.email_id == request.user.email
        elif hasattr(obj, 'email'):
            return obj.email == request.user.email
        elif hasattr(obj, 'payment_order_id') and hasattr(obj.payment_order_id, 'email_id'):
            return obj.payment_order_id.email_id == request.user.email
        else:
            return False

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    message = 'You do not have permissions for this request.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif hasattr(obj, 'email_id'):
            return obj.email_id == request.user.email
        elif hasattr(obj, 'email'):
            return obj.email == request.user.email
        elif hasattr(obj, 'payment_order_id') and hasattr(obj.payment_order_id, 'email_id'):
            return obj.payment_order_id.email_id == request.user.email
        else:
            return False

class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'You do not have permission for this request.'
    def has_permission(self, request, view):
         return bool(request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff)
