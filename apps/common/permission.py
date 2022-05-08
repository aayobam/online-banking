from rest_framework import permissions



class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
       return bool(request.user and request.user.is_superuser)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role == "Admin":
            return True
        return obj == user and user.role == "Customer"