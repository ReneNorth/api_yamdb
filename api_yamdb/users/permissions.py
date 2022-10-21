from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_superuser)


# class IsAdminOrSuperuser(BasePermission):
#     """Полный доступ ко всему толькоо для админов и суперпользователей.
#     Подходит для моделей Categories, Genres."""
#
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
#         if request.user.is_superuser or request.user.role == 'admin':
#             return True
#
#     def has_object_permission(self, request, view, obj):
#         if not request.user.is_authenticated:
#             return False
#         if request.user.is_superuser or request.user.role == 'admin':
#             return True


class TitleRoutePermission(BasePermission):
    """Доступ на чтение всем.
    Доступ к изменению объекта только админу или суперпользователю."""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.role == 'admin':
            return True


class ReviewsAndCommentsRoutePermission(BasePermission):
    """Доступ на чтение всем.
    Доступ к созданию всем кроме не аутентифицированных пользователей.
    Доступ к удалению и редактированию админам, модераторам,
    суперпользователям и авторам контента."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # if not request.user.is_authenticated:
        #     return False
        # TODO: у obj (моделей Comments, Review) будет поле author?
        if request.method in ['UPDATE', 'DELETE'] and request.user != obj.author:
            return False

        return True
