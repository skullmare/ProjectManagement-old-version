from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Project, Task, Budget, Result, Risk, ProjectMembership
from .serializers import ProjectSerializer, TaskSerializer, BudgetSerializer, ResultSerializer, RiskSerializer
from .permissions import IsManager, IsLeader, IsParticipant

# =====================
# PROJECT VIEWS
# =====================
class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_manager:
            Project.objects.all()
        return Project.objects.filter(projectmembership__user=self.request.user)
        

# class ProjectCreateView(generics.CreateAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def perform_create(self, serializer):

# class ProjectDetailView(generics.RetrieveAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticated, IsManager | IsLeader | IsParticipant]

#     def get_queryset(self):

# class ProjectUpdateView(generics.UpdateAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def get_queryset(self):

# class ProjectDeleteView(generics.DestroyAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def get_queryset(self):

# =====================
# TASK VIEWS
# =====================
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            if self.request.user.is_manager:
                return Task.objects.filter(project_id=project_id)
            return Task.objects.filter(project__projectmembership__user=self.request.user, project_id=project_id)
        except Exception as e:
            raise ValidationError(f"Ошибка при получении задач: {str(e)}")

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                project_id = self.kwargs['project_id']
                serializer.save(project_id=project_id)
            else:
                raise PermissionDenied("У вас недостаточно прав для создания задачи.")
        except Exception as e:
            raise ValidationError(f"Ошибка при создании задачи: {str(e)}")

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            if (self.request.user.is_manager or
                ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists() or
                ProjectMembership.objects.filter(user=self.request.user, role="participant", project=project_id).exists()):
                return Task.objects.filter(project_id=project_id)
            return Task.objects.none()
        except Exception as e:
            raise ValidationError(f"Ошибка при получении задачи: {str(e)}")

    def perform_update(self, serializer):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                serializer.save()
            else:
                raise PermissionDenied("У вас недостаточно прав для обновления задачи.")
        except Exception as e:
            raise ValidationError(f"Ошибка при обновлении задачи: {str(e)}")

    def perform_destroy(self, instance):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                instance.delete()
            else:
                raise PermissionDenied("У вас недостаточно прав для удаления задачи.")
        except Exception as e:
            raise ValidationError(f"Ошибка при удалении задачи: {str(e)}")


# =====================
# BUDGET VIEWS
# =====================
class BudgetListView(generics.ListAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            if self.request.user.is_manager:
                return Budget.objects.filter(project_id=project_id)
            return Budget.objects.filter(project__projectmembership__user=self.request.user, project_id=project_id)
        except Exception as e:
            raise ValidationError(f"Ошибка при получении бюджета: {str(e)}")

class BudgetCreateView(generics.CreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                project_id = self.kwargs['project_id']
                serializer.save(project_id=project_id)
            else:
                raise PermissionDenied("У вас недостаточно прав для создания бюджета.")
        except Exception as e:
            raise ValidationError(f"Ошибка при создании бюджета: {str(e)}")

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            if (self.request.user.is_manager or
                ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists() or
                ProjectMembership.objects.filter(user=self.request.user, role="participant", project=project_id).exists()):
                return Budget.objects.filter(project_id=project_id)
            return Budget.objects.none()
        except Exception as e:
            raise ValidationError(f"Ошибка при получении бюджета: {str(e)}")

    def perform_update(self, serializer):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                serializer.save()
            else:
                raise PermissionDenied("У вас недостаточно прав для обновления бюджета.")
        except Exception as e:
            raise ValidationError(f"Ошибка при обновлении бюджета: {str(e)}")

    def perform_destroy(self, instance):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                instance.delete()
            else:
                raise PermissionDenied("У вас недостаточно прав для удаления бюджета.")
        except Exception as e:
            raise ValidationError(f"Ошибка при удалении бюджета: {str(e)}")


# =====================
# RESULT VIEWS
# =====================
class ResultListView(generics.ListAPIView):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            if self.request.user.is_manager:
                return Result.objects.filter(project_id=project_id)
            return Result.objects.filter(project__projectmembership__user=self.request.user, project_id=project_id)
        except Exception as e:
            raise ValidationError(f"Ошибка при получении результата: {str(e)}")

class ResultCreateView(generics.CreateAPIView):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                project_id = self.kwargs['project_id']
                serializer.save(project_id=project_id)
            else:
                raise PermissionDenied("У вас недостаточно прав для создания результата.")
        except Exception as e:
            raise ValidationError(f"Ошибка при создании результата: {str(e)}")

class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            if (self.request.user.is_manager or
                ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists() or
                ProjectMembership.objects.filter(user=self.request.user, role="participant", project=project_id).exists()):
                return Result.objects.filter(project_id=project_id)
            return Result.objects.none()
        except Exception as e:
            raise ValidationError(f"Ошибка при получении результата: {str(e)}")

    def perform_update(self, serializer):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                serializer.save()
            else:
                raise PermissionDenied("У вас недостаточно прав для обновления результата.")
        except Exception as e:
            raise ValidationError(f"Ошибка при обновлении результата: {str(e)}")

    def perform_destroy(self, instance):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                instance.delete()
            else:
                raise PermissionDenied("У вас недостаточно прав для удаления результата.")
        except Exception as e:
            raise ValidationError(f"Ошибка при удалении результата: {str(e)}")


# =====================
# RISK VIEWS
# =====================
class RiskListView(generics.ListAPIView):
    serializer_class = RiskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            if self.request.user.is_manager:
                return Risk.objects.filter(project_id=project_id)
            return Risk.objects.filter(project__projectmembership__user=self.request.user, project_id=project_id)
        except Exception as e:
            raise ValidationError(f"Ошибка при получении рисков: {str(e)}")

class RiskCreateView(generics.CreateAPIView):
    serializer_class = RiskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                project_id = self.kwargs['project_id']
                serializer.save(project_id=project_id)
            else:
                raise PermissionDenied("У вас недостаточно прав для создания риска.")
        except Exception as e:
            raise ValidationError(f"Ошибка при создании риска: {str(e)}")

class RiskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            if (self.request.user.is_manager or
                ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists() or
                ProjectMembership.objects.filter(user=self.request.user, role="participant", project=project_id).exists()):
                return Risk.objects.filter(project_id=project_id)
            return Risk.objects.none()
        except Exception as e:
            raise ValidationError(f"Ошибка при получении риска: {str(e)}")

    def perform_update(self, serializer):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                serializer.save()
            else:
                raise PermissionDenied("У вас недостаточно прав для обновления риска.")
        except Exception as e:
            raise ValidationError(f"Ошибка при обновлении риска: {str(e)}")

    def perform_destroy(self, instance):
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
                instance.delete()
            else:
                raise PermissionDenied("У вас недостаточно прав для удаления риска.")
        except Exception as e:
            raise ValidationError(f"Ошибка при удалении риска: {str(e)}")
