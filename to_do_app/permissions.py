from rest_framework import permissions
class IsOwnerOfPlan(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit, view, delete, and create it.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user
    
class IsOwnerOfTask(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit view, delete, and create it.
    """
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        return obj.plan.owner == request.user