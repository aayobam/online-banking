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

    message = "Only super users and admins are allowed to access this page."

    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_superuser or user.role == "Admin")


class IsOwnerOrReadOnly(permissions.BasePermission):

    message = "You do not have permissions to access this page."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == user and user.role == "Customer"
