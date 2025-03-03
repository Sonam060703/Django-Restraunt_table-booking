# table_management/permissions.py
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a reservation or admins to view/modify.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is admin
        if request.user.is_admin:
            return True
            
        # Check if user is the owner of the reservation
        return obj.user == request.user