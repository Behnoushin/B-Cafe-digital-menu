from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsChefOrAdmin(BasePermission):
    """
    Only chefs or admins are allowed access (for creating and viewing).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['chef', 'admin']


class IsAdminOnly(BasePermission):
    """
    Only admins are allowed (for approving and editing items).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsChefAndNotApprovedOrAdmin(BasePermission):
    """
    Chefs are allowed to edit/delete only if the request is not approved yet.
    Admins always have access.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.method in SAFE_METHODS:
            return True
        if request.user.role == 'chef' and obj.chef == request.user and not obj.is_reviewed:
            return True
        return False
