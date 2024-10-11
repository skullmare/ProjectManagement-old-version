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
        if self.request.user.is_manager:
            Task.objects.all()
        return Task.objects.filter(project__projectmembership__user=self.request.user)

# class TaskCreateView(generics.CreateAPIView):
#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def perform_create(self, serializer):

# class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TaskSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def get_queryset(self):

# # =====================
# # BUDGET VIEWS
# # =====================
# class BudgetListView(generics.ListAPIView):
#     serializer_class = BudgetSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):

# class BudgetCreateView(generics.CreateAPIView):
#     serializer_class = BudgetSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def perform_create(self, serializer):

# class BudgetDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = BudgetSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def get_queryset(self):

# # =====================
# # RESULT VIEWS
# # =====================
# class ResultListView(generics.ListAPIView):
#     serializer_class = ResultSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):

# class ResultCreateView(generics.CreateAPIView):
#     serializer_class = ResultSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def perform_create(self, serializer):

# class ResultDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ResultSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def get_queryset(self):

# # =====================
# # RISK VIEWS
# # =====================
# class RiskListView(generics.ListAPIView):
#     serializer_class = RiskSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):

# class RiskCreateView(generics.CreateAPIView):
#     serializer_class = RiskSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def perform_create(self, serializer):

# class RiskDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = RiskSerializer
#     permission_classes = [permissions.IsAuthenticated, IsLeader]

#     def get_queryset(self):
