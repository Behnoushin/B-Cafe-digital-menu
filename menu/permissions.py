from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """"
    Only admins can perform write operations (POST, PUT, PATCH, DELETE).
    Others can only read (GET).
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff
    
    
class IsAdminOnly(BasePermission):
    """
    Only the admin user has access to all types of requests.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
    