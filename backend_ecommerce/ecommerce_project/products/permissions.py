from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for any user, but restrict write operations to admin users.
    """
    
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for any user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is admin
        return request.user and request.user.is_staff