from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Result, Project
from .serializers import ResultSerializer

class ResultListCreateView(generics.ListCreateAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user.is_manager or user in project.leaders.all() or user in project.participants.all():
            return Result.objects.filter(project_id=project_id)
        raise serializers.ValidationError("У вас недостаточно прав для доступа к результатам проекта.")

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
            raise serializers.ValidationError("У вас недостаточно прав для создания результата.")


class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user.is_manager or user in project.leaders.all() or user in project.participants.all():
            return Result.objects.filter(project_id=project_id)
        raise serializers.ValidationError("У вас недостаточно прав для доступа к результату проекта.")

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
            raise serializers.ValidationError("У вас недостаточно прав для изменения результата.")

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
            raise serializers.ValidationError("У вас недостаточно прав для удаления результата.")
