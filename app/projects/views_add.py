from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import LeaderSerializer, ParticipantSerializer

class ProjectLeaderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def add_leader(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        # Проверяем, является ли текущий пользователь лидером проекта
        if request.user not in project.leaders.all():
            return Response({"detail": "У вас нет прав для добавления руководителей."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LeaderSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectParticipantViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def add_participant(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        # Проверяем, является ли текущий пользователь лидером проекта
        if request.user not in project.leaders.all():
            return Response({"detail": "У вас нет прав для добавления участников."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ParticipantSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
