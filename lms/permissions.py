from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='managers').exists():
            return True


class IsNotManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='managers').exists():
            return False
        return True


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated()
        elif view.action in ['create', 'delete']:
            return request.user.is_authenticated() and not request.user.groups.filter(name='managers').exists()
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated() and request.user.groups.filter(name='managers').exists()
        else:
            return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated():
            return False

        if view.action == 'retrieve':
            return obj == request.user or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_admin
        elif view.action == 'destroy':
            return request.user.is_admin
        else:
            return False


class IsLessonOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.lesson_owner:
            return True
        return False


class IsCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.lesson_owner:
            return True
        return False
