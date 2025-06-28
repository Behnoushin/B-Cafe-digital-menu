from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrCreateOnly(BasePermission):
    """
    - All users (even guests) can make new reservations (POST).
    - Only admins (users with is_staff=True) can view, edit or delete reservations.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_staff
        if request.method == 'POST':
            return True
        return request.user and request.user.is_staff