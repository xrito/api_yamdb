from rest_framework import permissions
from ..users.models import User


class CanReadPermission(permissions.BasePermission):
    """Класс пермишена для доступа на чтение."""
    def has_permission(self, request, view):
        """Метод проверяет тип запроса. Если он на чтение - разрешаем доступ"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class CanEditUserContentPermission(permissions.BasePermission):
    """Класс пермишена для доступа к изменению контента,
    генерируемого пользователями. Такой контент могут изменять модераторы,
    администраторы или авторы"""
    def has_object_permission(self, request, view, obj):
        """Метод проверяет сначала, имеет ли пользователь
        группу модератора или администратора,
        а затем проверяет является ли пользователь автором поста"""
        if request.user.role in (User.MODERATOR, User.ADMIN):
            return True
        return obj.author == request.user


class CanEditAdminContent(permissions.BasePermission):
    """Класс пермишена для доступа к изменению контента администратора.
    Такой контент могут изменять только администраторы и суперпользователь."""
    def has_object_permission(self, request, view, obj):
        """Метод проверяет является ли пользователь
        администратором или суперпользователем"""
        if request.user.role == User.ADMIN or request.user.is_superuser:
            return True
