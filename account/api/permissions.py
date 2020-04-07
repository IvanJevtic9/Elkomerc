from rest_framework import permissions

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

        return obj.user.core_filters.get('email').email == request.user.email    