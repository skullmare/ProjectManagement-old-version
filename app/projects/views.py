from rest_framework import generics
from .models import Project, Task, Budget, Result, Risk, ProjectMembership
from .serializers import ProjectSerializer, TaskSerializer, BudgetSerializer, ResultSerializer, RiskSerializer
from .permissions import IsManager, IsLeader, IsParticipant

class BaseListView(generics.ListAPIView):
    model = None
    serializer_class = None

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if self.request.user.is_manager:
            return self.model.objects.filter(project_id=project_id)
        elif self.request.user.is_leader:
            return self.model.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        elif self.request.user.is_participant:
            return self.model.objects.filter(project_id=project_id, project__memberships__user=self.request.user)
        return self.model.objects.none()


class BaseCreateView(generics.CreateAPIView):
    model = None
    serializer_class = None
    permission_classes = [IsLeader]

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id=project_id)
        serializer.save(project=project)


class BaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = None
    serializer_class = None
    permission_classes = [IsLeader]

    def get_queryset(self):
        return self.model.objects.all()


# =====================
# PROJECT VIEWS
# =====================
class ProjectListView(BaseListView):
    model = Project
    serializer_class = ProjectSerializer


class ProjectCreateView(BaseCreateView):
    model = Project
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        project = serializer.save()
        ProjectMembership.objects.create(user=self.request.user, project=project, role='leader')


class ProjectDetailView(BaseDetailView):
    model = Project
    serializer_class = ProjectSerializer
    permission_classes = [IsManager | IsLeader | IsParticipant]


class ProjectUpdateView(BaseDetailView):
    model = Project
    serializer_class = ProjectSerializer


class ProjectDeleteView(BaseDetailView):
    model = Project
    serializer_class = ProjectSerializer


# =====================
# TASK VIEWS
# =====================
class TaskListView(BaseListView):
    model = Task
    serializer_class = TaskSerializer


class TaskCreateView(BaseCreateView):
    model = Task
    serializer_class = TaskSerializer


class TaskDetailView(BaseDetailView):
    model = Task
    serializer_class = TaskSerializer


# =====================
# BUDGET VIEWS
# =====================
class BudgetListView(BaseListView):
    model = Budget
    serializer_class = BudgetSerializer


class BudgetCreateView(BaseCreateView):
    model = Budget
    serializer_class = BudgetSerializer


class BudgetDetailView(BaseDetailView):
    model = Budget
    serializer_class = BudgetSerializer


# =====================
# RESULT VIEWS
# =====================
class ResultListView(BaseListView):
    model = Result
    serializer_class = ResultSerializer


class ResultCreateView(BaseCreateView):
    model = Result
    serializer_class = ResultSerializer


class ResultDetailView(BaseDetailView):
    model = Result
    serializer_class = ResultSerializer


# =====================
# RISK VIEWS
# =====================
class RiskListView(BaseListView):
    model = Risk
    serializer_class = RiskSerializer


class RiskCreateView(BaseCreateView):
    model = Risk
    serializer_class = RiskSerializer


class RiskDetailView(BaseDetailView):
    model = Risk
    serializer_class = RiskSerializer
