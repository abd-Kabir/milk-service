from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list' or view.action == 'retrieve':
            return True
        return False
