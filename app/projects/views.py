from rest_framework import generics
from .models import Project, Task, Budget, Result, Risk, ProjectMembership
from .serializers import ProjectSerializer, TaskSerializer, BudgetSerializer, ResultSerializer, RiskSerializer
from .permissions import IsManager, IsLeader, IsParticipant

# =====================
# PROJECT VIEWS
# =====================
class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.is_manager:
            return Project.objects.all()
        elif self.request.user.is_leader:
            return Project.objects.filter(memberships__user=self.request.user)
        elif self.request.user.is_participant:
            return Project.objects.filter(memberships__user=self.request.user)
        return Project.objects.none()

class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsLeader]

    def perform_create(self, serializer):
        project = serializer.save()
        ProjectMembership.objects.create(user=self.request.user, project=project, role='leader')

class ProjectDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsManager | IsLeader | IsParticipant]

    def get_queryset(self):
        return Project.objects.all()

class ProjectUpdateView(generics.UpdateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsLeader]

    def get_queryset(self):
        return Project.objects.all()

class ProjectDeleteView(generics.DestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsLeader]

    def get_queryset(self):
        return Project.objects.all()

# =====================
# TASK VIEWS
# =====================
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if self.request.user.is_manager:
            return Task.objects.filter(project_id=project_id)
        elif self.request.user.is_leader:
            return Task.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        elif self.request.user.is_participant:
            return Task.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        return Task.objects.none()

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsLeader]

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        # Просто сохраняем проект в сериализаторе, проверка на уровне permissions
        serializer.save(project=project)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsLeader]

    def get_queryset(self):
        return Task.objects.all()

# =====================
# BUDGET VIEWS
# =====================
class BudgetListView(generics.ListAPIView):
    serializer_class = BudgetSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if self.request.user.is_manager:
            return Budget.objects.filter(project_id=project_id)
        elif self.request.user.is_leader:
            return Budget.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        elif self.request.user.is_participant:
            return Budget.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        return Budget.objects.none()

class BudgetCreateView(generics.CreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsLeader]

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsLeader]

    def get_queryset(self):
        return Budget.objects.all()

# =====================
# RESULT VIEWS
# =====================
class ResultListView(generics.ListAPIView):
    serializer_class = ResultSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if self.request.user.is_manager:
            return Result.objects.filter(project_id=project_id)
        elif self.request.user.is_leader:
            return Result.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        elif self.request.user.is_participant:
            return Result.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        return Result.objects.none()

class ResultCreateView(generics.CreateAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsLeader]

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsLeader]

    def get_queryset(self):
        return Result.objects.all()

# =====================
# RISK VIEWS
# =====================
class RiskListView(generics.ListAPIView):
    serializer_class = RiskSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if self.request.user.is_manager:
            return Risk.objects.filter(project_id=project_id)
        elif self.request.user.is_leader:
            return Risk.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        elif self.request.user.is_participant:
            return Risk.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        return Risk.objects.none()

class RiskCreateView(generics.CreateAPIView):
    serializer_class = RiskSerializer
    permission_classes = [IsLeader]

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)

class RiskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiskSerializer
    permission_classes = [IsLeader]

    def get_queryset(self):
        return Risk.objects.all()
