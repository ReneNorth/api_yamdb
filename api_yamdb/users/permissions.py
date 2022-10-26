from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import User


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return (request.user.is_authenticated
                and request.user.role == 'admin')
        
        

class CreateListUsersPermission(BasePermission):
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'admin'
                or request.user.is_superuser
                or request.user.is_staff)
        
    
    def has_object_permission(self, request, view, obj):
        # print(request.user.role == 'admin'
        #       or request.user.is_superuser
        #       or request.user.is_staff)
        return (request.user.role == 'admin'
                or request.user.is_superuser
                or request.user.is_staff)



class TempPermission(BasePermission):
    pass
#     def has_permission(self, request, view):
#         print('user has_permission temp permission')
#         print(request.method)
#         return True
    
#     def has_object_permission(self, request, view, obj):
#         print('user has_permission2')
#         return True

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        print('user has_permission')
        print(User.objects.all())
        # print(dir(request.user))
        # print(request.user.is_superuser or request.user.is_staff)
        # print(request.user.role, '<- роль юзера')
        # print(request.data)
        # print(request.user.is_superuser)
        # print(request.user.is_staff)
        # print(request.user.is_active)
        print(request.user.is_authenticated and request.user.is_superuser)
        
        return bool(request.user and request.user.is_superuser)
        # # print(bool(request.user.is_superuser or request.user.is_staff))
        # print(request.user.is_authenticated and request.user.is_superuser)
        # return bool(request.user.is_superuser or request.user.is_staff)
        # return bool(request.user.is_superuser)
        # return (request.user.is_authenticated and request.user.is_superuser)

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
        try:
            return (
                request.method in SAFE_METHODS or request.user.role == 'admin'
            )
        except AttributeError:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            if (
                request.method == 'GET'
                or request.user.is_superuser
                or request.user.role == 'admin'
            ):
                return True
        except AttributeError:
            return False


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
        if (
            request.method in ['UPDATE', 'DELETE']
            and request.user != obj.author
        ):
            return False

        return True
