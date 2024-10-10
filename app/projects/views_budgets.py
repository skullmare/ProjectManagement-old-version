from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from .models import Budget, Project
from .serializers import BudgetSerializer

class BudgetListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user.is_manager or user in project.leaders.all() or user in project.participants.all():
            return Budget.objects.filter(project_id=project_id)
        raise serializers.ValidationError("У вас недостаточно прав для доступа к бюджетам проекта.")

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
            raise serializers.ValidationError("У вас недостаточно прав для создания бюджета.")


class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        project_id = self.kwargs['project_id']
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Проект не найден.")

        if user.is_manager or user in project.leaders.all() or user in project.participants.all():
            return Budget.objects.filter(project_id=project_id)
        raise serializers.ValidationError("У вас недостаточно прав для доступа к бюджету проекта.")

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
            raise serializers.ValidationError("У вас недостаточно прав для изменения бюджета.")

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
            raise serializers.ValidationError("У вас недостаточно прав для удаления бюджета.")
