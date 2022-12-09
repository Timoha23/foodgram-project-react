from rest_framework import permissions


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(f'self: {self}\nrequest: {request}\nview: {view}\nobj: {obj}')
        return request.method in permissions.SAFE_METHODS or (
            obj.author == request.user
            or request.user.is_superuser
        )
