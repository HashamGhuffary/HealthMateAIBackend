from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    """
    Permission class to check if the user is a doctor.
    """
    message = "Only doctors are allowed to perform this action."
    
    def has_permission(self, request, view):
        # Always allow during schema generation
        if getattr(view, 'swagger_fake_view', False):
            return True
        return request.user and request.user.is_authenticated and request.user.is_doctor


class IsPatient(permissions.BasePermission):
    """
    Permission class to check if the user is a patient.
    """
    message = "Only patients are allowed to perform this action."
    
    def has_permission(self, request, view):
        # Always allow during schema generation
        if getattr(view, 'swagger_fake_view', False):
            return True
        return request.user and request.user.is_authenticated and request.user.is_patient


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    message = "You must be the owner of this object to perform this action."
    
    def has_object_permission(self, request, view, obj):
        # Always allow during schema generation
        if getattr(view, 'swagger_fake_view', False):
            return True
            
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner
        return obj.user == request.user 