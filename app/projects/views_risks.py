from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Risk, Project
from .serializers import RiskSerializer

class RiskListCreateView(generics.ListCreateAPIView):
    serializer_class = RiskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user.is_manager or user in project.leaders.all() or user in project.participants.all():
            return Risk.objects.filter(project_id=project_id)
        raise serializers.ValidationError("У вас недостаточно прав для доступа к рискам проекта.")

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
            raise serializers.ValidationError("У вас недостаточно прав для создания риска.")


class RiskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user.is_manager or user in project.leaders.all() or user in project.participants.all():
            return Risk.objects.filter(project_id=project_id)
        raise serializers.ValidationError("У вас недостаточно прав для доступа к риску проекта.")

    def get_object(self):
        queryset = self.get_queryset()
        risk_id = self.kwargs['pk']
        try:
            return queryset.get(pk=risk_id)
        except Risk.DoesNotExist:
            raise serializers.ValidationError("Риск не найден.")

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
            raise serializers.ValidationError("У вас недостаточно прав для изменения риска.")

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
            raise serializers.ValidationError("У вас недостаточно прав для удаления риска.")
