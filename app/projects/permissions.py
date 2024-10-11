from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Разрешение для менеджеров, позволяющее доступ ко всем проектам.
    """
    
    def has_permission(self, request, view):
        return request.user.is_manager
class IsLeader(permissions.BasePermission):
    """
    Разрешение для лидеров, позволяющее доступ к проектам, в которых они являются руководителями.
    """
    
    def has_permission(self, request, view):
        return request.user.is_leader

    def has_object_permission(self, request, view, obj):
        # Используем project для доступа к memberships
        return obj.project.memberships.filter(user=request.user, role='leader').exists()

class IsParticipant(permissions.BasePermission):
    """
    Разрешение для участников, позволяющее доступ к проектам, в которых они участвуют.
    """

    def has_object_permission(self, request, view, obj):
        # Используем project для доступа к memberships
        return obj.project.memberships.filter(user=request.user, role='participant').exists()

