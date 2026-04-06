from rest_framework import permissions


# permissions.py
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # যদি ইউজার সুপার এডমিন হয়, তবে তাকে সব পারমিশন দিয়ে দাও
        if request.user and request.user.is_superuser:
            return True
            
        # অন্যথায় রোল চেক করো
        return request.user.is_authenticated and request.user.role in ['ADMIN']
    

class IsAdminOrTL(permissions.BasePermission):
    def has_permission(self, request, view):
        # যদি ইউজার সুপার এডমিন হয়, তবে তাকে সব পারমিশন দিয়ে দাও
        if request.user and request.user.is_superuser:
            return True
            
        # অন্যথায় রোল চেক করো
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'TL']
    


class IsTL(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'TL'

class IsSR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SR'
    


    
