from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Task, Budget, Result, Risk, ProjectMembership
from .serializers import ProjectSerializer, TaskSerializer, BudgetSerializer, ResultSerializer, RiskSerializer, ProjectMembershipSerializer

class BaseProjectAPIView:
    def check_project_permissions(self, project_id):
        if not (self.request.user.is_manager or
                ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists() or
                ProjectMembership.objects.filter(user=self.request.user, role="participant", project=project_id).exists()):
            raise PermissionDenied("У вас недостаточно прав для доступа к данному проекту.")
    def check_project_permissions_leader(self, project_id):
        return ProjectMembership.objects.filter(user=self.request.user, role="leader", project=project_id).exists()
    
# =====================
# BASE VIEWS FOR PARAMETERS
# =====================

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
            if self.check_project_permissions_leader(project_id):
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
            if self.check_project_permissions_leader(project_id):
                serializer.save()
            else:
                raise PermissionDenied("У вас недостаточно прав для обновления записи.")
        except Exception as e:
            raise ValidationError(f"Ошибка при обновлении записи: {str(e)}")

    def perform_destroy(self, instance):
        project_id = self.kwargs['project_id']
        try:
            if self.check_project_permissions_leader(project_id):
                instance.delete()
            else:
                raise PermissionDenied("У вас недостаточно прав для удаления записи.")
        except Exception as e:
            raise ValidationError(f"Ошибка при удалении записи: {str(e)}")

# =====================
# PROJECT VIEWS
# =====================
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'
    max_page_size = 100  # Максимальное количество элементов на странице

class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']  # Поле для фильтрации

    def get_queryset(self):
        queryset = Project.objects.all() if self.request.user.is_manager \
            else Project.objects.filter(projectmembership__user=self.request.user)
        
        # Дополнительная фильтрация по частичному совпадению названия
        name_filter = self.request.query_params.get('name', None)
        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)
            print(queryset.filter(name__icontains=name_filter).query)
            
        return queryset

class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_leader:
            project = serializer.save()
            ProjectMembership.objects.create(user=self.request.user, project=project, role='leader')
        else:
            raise PermissionDenied("У вас нет прав на создание проекта.")

class ProjectDetailView(generics.RetrieveAPIView, BaseProjectAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['pk']
        self.check_project_permissions(project_id)
        return Project.objects.filter(id=project_id)

class ProjectUpdateView(generics.UpdateAPIView, BaseProjectAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
            
    def get_queryset(self):
        project_id = self.kwargs['pk']
        self.check_project_permissions(project_id)
        return Project.objects.filter(id=project_id)
    
    def perform_update(self, serializer):
        project_id = self.kwargs['pk']
        if self.check_project_permissions_leader(project_id):
            serializer.save()
        else:
            raise PermissionDenied("У вас недостаточно прав для обновления проекта.")

class ProjectDeleteView(generics.DestroyAPIView, BaseProjectAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['pk']
        self.check_project_permissions(project_id)
        return Project.objects.filter(id=project_id)
    
    def perform_destroy(self, instance):
        project_id = instance.id
        if self.check_project_permissions_leader(project_id):
            instance.delete()
        else:
            raise PermissionDenied("У вас недостаточно прав для удаления проекта.")

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

# =====================
# MEMBERS VIEWS
# =====================
class ProjectMemberListView(BaseListView):
    queryset_class = ProjectMembership.objects
    serializer_class = ProjectMembershipSerializer

class ProjectMemberCreateView(BaseCreateView):
    queryset_class = ProjectMembership.objects
    serializer_class = ProjectMembershipSerializer

class ProjectMemberDetailView(BaseDetailView):
    queryset_class = ProjectMembership.objects
    serializer_class = ProjectMembershipSerializer