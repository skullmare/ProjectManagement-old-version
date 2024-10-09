from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import serializers
from .models import Project
from .serializers import ProjectSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            return Project.objects.all()  # Менеджер может видеть все проекты
        # Возвращает проекты, в которых пользователь является лидер или участник
        return Project.objects.filter(leaders=user) | Project.objects.filter(participants=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_leader:
            serializer.save(leaders=[user])  # Устанавливаем текущего пользователя как лидера проекта
        else:
            raise serializers.ValidationError("У вас недостаточно прав для создания проекта.")

class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user in project.participants.all() or request.user in project.leaders.all() or request.user.is_manager:
            serializer = self.get_serializer(project)
            return Response(serializer.data)
        else:
            return Response({"detail": "У вас недостаточно прав для просмотра проекта."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user.is_leader:  # Только лидеры могут обновлять проект
            serializer = self.get_serializer(project, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({"detail": "У вас недостаточно прав для обновления проекта."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user.is_leader:  # Только лидеры могут удалять проект
            self.perform_destroy(project)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "У вас недостаточно прав для удаления проекта."}, status=status.HTTP_403_FORBIDDEN)
