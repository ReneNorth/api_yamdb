from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModeratorPermission(BasePermission):
    """Доступ к изменению контента только для автора контента."""
    required_role = 'moderator'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if self.required_role is None:
            return False
        if request.user.role == self.required_role:
            return True
        return False


class OwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            return obj.user == request.user
        return True


# class UserRolePermission(BasePermission):
#     """Доступ к изменению контента только для автора контента."""
#
#     def has_permission(self, request, view):
#         return (request.method in SAFE_METHODS
#                 or request.user.is_authenticated)
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         return obj.author == request.user
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['PUT', 'PATCH', 'DELETE']:
#             return obj.author == request.user
#         if request.method == 'POST':
#             return request.user.is_authenticated
#         return True
#
#
# def _is_fit_role(user, role_name):
#     """
#     Takes a user and a group name, and returns `True` if the user is in that group.
#     """
#     if user.role == role_name:
#         return True
#     return False
#
#
# def _has_role_permission(user, required_groups):
#     return any([_is_fit_role(user, group_name) for group_name in required_groups])
#
#
# class IsLoggedInUserOrAdmin(BasePermission):
#     # group_name for super admin
#     required_groups = ['admin']
#
#     def has_object_permission(self, request, view, obj):
#         has_role_permission = _has_role_permission(request.user, self.required_groups)
#         if self.required_groups is None:
#             return False
#         return obj == request.user or has_role_permission
#
#
# class IsAdminUser(BasePermission):
#     # group_name for super admin
#     required_groups = ['admin']
#
#     def has_permission(self, request, view):
#         has_role_permission = _has_role_permission(request.user, self.required_groups)
#         return request.user and has_role_permission
#
#     def has_object_permission(self, request, view, obj):
#         has_role_permission = _has_role_permission(request.user, self.required_groups)
#         return request.user and has_role_permission
#
#
# class IsAdminOrAnonymousUser(BasePermission):
#     required_groups = ['admin', 'anonymous']
#
#     def has_permission(self, request, view):
#         has_role_permission = _has_role_permission(request.user, self.required_groups)
#         return request.user and has_role_permission
