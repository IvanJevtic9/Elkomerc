from rest_framework import permissions
from rest_framework import authentication
class AnonPermissionOnly(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message = 'You are already authenticated, please log out.'
    def has_permission(self, request, view):
        return not request.user.is_authenticated

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners og an object to edit it.
    Assumes the model instance hasn an 'owner' attribute.
    """
    message = 'You do not have permissions to update.'
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        # so we will always allow GET , HEAD or OPTIONS requests.
        if request.user.is_anonymous:
            return False

        return obj.user.core_filters.get('email').email == request.user.email

class AdminAuthenticationPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser
        return False            