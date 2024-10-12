from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Project, Task, Budget, Result, Risk, ProjectMembership
from .serializers import ProjectSerializer, TaskSerializer, BudgetSerializer, ResultSerializer, RiskSerializer

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

class BaseProjectAPIView:
    def check_project_permissions(self, project_id):
        if not (self.request.user.is_manager or
                ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists() or
                ProjectMembership.objects.filter(user=self.request.user, role="participant", project=project_id).exists()):
            raise PermissionDenied("У вас недостаточно прав для доступа к данному проекту.")

class BaseListView(generics.ListAPIView, BaseProjectAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        try:
            self.check_project_permissions(project_id)
            return self.queryset_class.filter(project_id=project_id)
        except Exception as e:
            raise ValidationError(f"Ошибка при получении данных: {str(e)}")

class BaseCreateView(generics.CreateAPIView, BaseProjectAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists():
                serializer.save(project_id=project_id)
            else:
                raise PermissionDenied("У вас недостаточно прав для создания записи.")
        except Exception as e:
            raise ValidationError(f"Ошибка при создании записи: {str(e)}")

class BaseDetailView(generics.RetrieveUpdateDestroyAPIView, BaseProjectAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        id = self.kwargs['pk']
        try:
            self.check_project_permissions(project_id)
            return self.queryset_class.filter(project_id=project_id, id=id)
        except Exception as e:
            raise ValidationError(f"Ошибка при получении записи: {str(e)}")

    def perform_update(self, serializer):
        project_id = self.kwargs['project_id']
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists():
                serializer.save()
            else:
                raise PermissionDenied("У вас недостаточно прав для обновления записи.")
        except Exception as e:
            raise ValidationError(f"Ошибка при обновлении записи: {str(e)}")

    def perform_destroy(self, instance):
        project_id = self.kwargs['project_id']
        try:
            if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists():
                instance.delete()
            else:
                raise PermissionDenied("У вас недостаточно прав для удаления записи.")
        except Exception as e:
            raise ValidationError(f"Ошибка при удалении записи: {str(e)}")

# =====================
# TASK VIEWS
# =====================
class TaskListView(BaseListView):
    serializer_class = TaskSerializer
    queryset_class = Task.objects

class TaskCreateView(BaseCreateView):
    serializer_class = TaskSerializer

class TaskDetailView(BaseDetailView):
    serializer_class = TaskSerializer
    queryset_class = Task.objects

# =====================
# BUDGET VIEWS
# =====================
class BudgetListView(BaseListView):
    serializer_class = BudgetSerializer
    queryset_class = Budget.objects

class BudgetCreateView(BaseCreateView):
    serializer_class = BudgetSerializer

class BudgetDetailView(BaseDetailView):
    serializer_class = BudgetSerializer
    queryset_class = Budget.objects

# =====================
# RESULT VIEWS
# =====================
class ResultListView(BaseListView):
    serializer_class = ResultSerializer
    queryset_class = Result.objects

class ResultCreateView(BaseCreateView):
    serializer_class = ResultSerializer

class ResultDetailView(BaseDetailView):
    serializer_class = ResultSerializer
    queryset_class = Result.objects

# =====================
# RISK VIEWS
# =====================
class RiskListView(BaseListView):
    serializer_class = RiskSerializer
    queryset_class = Risk.objects

class RiskCreateView(BaseCreateView):
    serializer_class = RiskSerializer

class RiskDetailView(BaseDetailView):
    serializer_class = RiskSerializer
    queryset_class = Risk.objects