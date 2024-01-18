from rest_framework import permissions
import logging
from core.settings import base
from django.core import cache


class IsIdempotent(permissions.BasePermission):
    
    message = 'Duplicate request detected.'

    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        ival = request.META.get('HTTP_X_IDEMPOTENCY_KEY')
        if ival is None:
            return True
        ival = ival[:128]
        key = 'idemp-{}-{}'.format(request.user.pk, ival)
        is_idempotent = bool(cache.add(key, 'yes', base.IDEMPOTENCY_TIMEOUT))
        if not is_idempotent:
            logging.info(u'Duplicate request (non-idempotent): %s', key)
        return is_idempotent
        

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role == "Admin":
            return True
        return obj == user and user.role == "Customer"
        
