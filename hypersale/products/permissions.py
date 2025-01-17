from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'POST':  # Allow only admin users to create discounts
            return request.user and request.user.is_staff
        return True 
