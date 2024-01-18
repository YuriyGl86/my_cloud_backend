from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False

        user = request.user
        requested_user_id = request.query_params.get('id', None)
        if requested_user_id and user.is_staff or user.id == requested_user_id:
            return True
        elif requested_user_id:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user == obj.owner or request.user.is_staff:
            return True
        else:
            return False
