from rest_framework import generics, permissions
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
        if self.request.user.is_manager:
            Task.objects.all(project_id=project_id)
        return Task.objects.filter(project__projectmembership__user=self.request.user, project_id=project_id)

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            project_id = self.kwargs['project_id']
            serializer.save(project_id=project_id)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if (self.request.user.is_manager or
            ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists() or
            ProjectMembership.objects.filter(user=self.request.user, role="participant", project=project_id).exists()):
            return Task.objects.filter(project_id=project_id)
        return Task.objects.none()

    def perform_update(self, serializer):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            serializer.save()

    def perform_destroy(self, instance):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            instance.delete()
    
  # =====================
# BUDGET VIEWS
# =====================
class BudgetListView(generics.ListAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Budget.objects.filter(project_id=project_id)

class BudgetCreateView(generics.CreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            project_id = self.kwargs['project_id']
            serializer.save(project_id=project_id)

class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists():
            return Budget.objects.filter(project_id=project_id)
        return Budget.objects.none()

    def perform_update(self, serializer):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            serializer.save()

    def perform_destroy(self, instance):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            instance.delete()

# =====================
# RESULT VIEWS
# =====================
class ResultListView(generics.ListAPIView):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Result.objects.filter(project_id=project_id)

class ResultCreateView(generics.CreateAPIView):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            project_id = self.kwargs['project_id']
            serializer.save(project_id=project_id)

class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists():
            return Result.objects.filter(project_id=project_id)
        return Result.objects.none()

    def perform_update(self, serializer):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            serializer.save()

    def perform_destroy(self, instance):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            instance.delete()

# =====================
# RISK VIEWS
# =====================
class RiskListView(generics.ListAPIView):
    serializer_class = RiskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Risk.objects.filter(project_id=project_id)

class RiskCreateView(generics.CreateAPIView):
    serializer_class = RiskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            project_id = self.kwargs['project_id']
            serializer.save(project_id=project_id)

class RiskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RiskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists():
            return Risk.objects.filter(project_id=project_id)
        return Risk.objects.none()

    def perform_update(self, serializer):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            serializer.save()

    def perform_destroy(self, instance):
        if ProjectMembership.objects.filter(user=self.request.user, role="leader", project=self.kwargs['project_id']).exists():
            instance.delete()
