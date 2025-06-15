from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Project, ProjectMembership, Budget, Risk, Result, Task
from django.contrib.auth import get_user_model

User = get_user_model()

class ProjectResource(resources.ModelResource):
    # Кастомные поля
    total_budget = fields.Field(column_name='total_budget', attribute='total_budget')
    member_count = fields.Field(column_name='member_count', attribute='member_count')
    task_count = fields.Field(column_name='task_count', attribute='task_count')
    risk_count = fields.Field(column_name='risk_count', attribute='risk_count')
    members = fields.Field(column_name='members', attribute='members')
    tasks = fields.Field(column_name='tasks', attribute='tasks')
    
    class Meta:
        model = Project
        fields = ('id', 'name', 'client', 'curator', 'purpose', 'description', 
                 'start_date', 'end_date', 'total_budget', 'member_count', 
                 'task_count', 'risk_count', 'members', 'tasks')
        export_order = fields
        widgets = {
            'start_date': {'format': '%d.%m.%Y'},
            'end_date': {'format': '%d.%m.%Y'},
        }

    def get_export_queryset(self):
        """Кастомизация queryset для экспорта"""
        return self._meta.model.objects.all().prefetch_related(
            'members', 'tasks', 'risks', 'budgets'
        )

    def dehydrate_total_budget(self, project):
        """Кастомизация поля total_budget"""
        budgets = project.budgets.all()
        if budgets:
            total = sum(b.amount for b in budgets)
            years = ", ".join(str(b.year) for b in budgets)
            return f"{total} ({years})"
        return "Нет данных"

    def dehydrate_member_count(self, project):
        """Кастомизация поля member_count"""
        return project.members.count()

    def dehydrate_task_count(self, project):
        """Кастомизация поля task_count"""
        return project.tasks.count()

    def dehydrate_risk_count(self, project):
        """Кастомизация поля risk_count"""
        return project.risks.count()

    def dehydrate_members(self, project):
        """Кастомизация поля members"""
        members = []
        for membership in project.projectmembership_set.all():
            members.append(f"{membership.user.email} ({membership.role})")
        return ", ".join(members)

    def dehydrate_tasks(self, project):
        """Кастомизация поля tasks"""
        tasks = []
        for task in project.tasks.all():
            tasks.append(f"{task.name} ({task.status})")
        return ", ".join(tasks)

    def get_member_count(self, obj):
        """Альтернативный метод получения количества участников"""
        return obj.members.count()

    def get_task_count(self, obj):
        """Альтернативный метод получения количества задач"""
        return obj.tasks.count()

    def get_risk_count(self, obj):
        """Альтернативный метод получения количества рисков"""
        return obj.risks.count()


class TaskResource(resources.ModelResource):
    project_name = fields.Field(column_name='project_name', attribute='project__name')
    assigned_users = fields.Field(column_name='assigned_users', attribute='assigned_users')
    duration = fields.Field(column_name='duration', attribute='duration')
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'project_name', 'description', 'start_date', 
                 'end_date', 'status', 'assigned_users', 'duration')
        export_order = fields
        widgets = {
            'start_date': {'format': '%d.%m.%Y'},
            'end_date': {'format': '%d.%m.%Y'},
        }

    def dehydrate_assigned_users(self, task):
        """Кастомизация поля assigned_users"""
        return ", ".join(user.email for user in task.assigned_users.all())

    def dehydrate_duration(self, task):
        """Кастомизация поля duration"""
        if task.start_date and task.end_date:
            return (task.end_date - task.start_date).days
        return None

    def get_duration(self, obj):
        """Альтернативный метод получения длительности"""
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None


class BudgetResource(resources.ModelResource):
    project_name = fields.Field(column_name='project_name', attribute='project__name')
    formatted_amount = fields.Field(column_name='formatted_amount', attribute='formatted_amount')
    
    class Meta:
        model = Budget
        fields = ('id', 'project_name', 'year', 'amount', 'formatted_amount')
        export_order = fields

    def dehydrate_formatted_amount(self, budget):
        """Кастомизация поля formatted_amount"""
        return f"${budget.amount:,.2f}"

    def get_formatted_amount(self, obj):
        """Альтернативный метод получения отформатированной суммы"""
        return f"${obj.amount:,.2f}" 