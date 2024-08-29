from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit or delete objects.
    """

    def has_permission(self, request, view):
        # Allow read-only requests for unauthenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Only admins can perform write operations
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners to edit or delete objects.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only requests for unauthenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Allow owners to edit or delete their own objects
        return request.user == obj.owner
