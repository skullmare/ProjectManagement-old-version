from rest_framework.permissions import BasePermission
from .models import ProjectMembership, Project

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

class IsLeader(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_leader
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.memberships.get(role='leader').user

class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_participant
    
    def has_object_permission(self, request, view, obj):
        return obj.memberships.filter(user=request.user).exists()