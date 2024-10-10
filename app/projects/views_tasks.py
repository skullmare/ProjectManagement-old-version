from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Project
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user.is_manager or user in project.leaders.all() or user in project.participants.all():
            return Task.objects.filter(project_id=project_id)
        raise serializers.ValidationError("У вас недостаточно прав для доступа к задачам проекта.")

    def perform_create(self, serializer):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user in project.leaders.all():
            serializer.save(project_id=project_id)
        else:
            raise serializers.ValidationError("У вас недостаточно прав для создания задачи.")


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user.is_manager or user in project.leaders.all() or user in project.participants.all():
            return Task.objects.filter(project_id=project_id)
        raise serializers.ValidationError("У вас недостаточно прав для доступа к задаче проекта.")

    def get_object(self):
        queryset = self.get_queryset()
        task_id = self.kwargs['pk']
        try:
            return queryset.get(pk=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError("Задача не найдена.")

    def perform_update(self, serializer):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user in project.leaders.all():
            serializer.save()
        else:
            raise serializers.ValidationError("У вас недостаточно прав для изменения задачи.")

    def perform_destroy(self, instance):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user in project.leaders.all():
            instance.delete()
        else:
            raise serializers.ValidationError("У вас недостаточно прав для удаления задачи.")
