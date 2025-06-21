from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Budget, Project, ProjectMembership, Result, Risk, Task
from .resources import BudgetResource, ProjectResource, TaskResource


class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 1
    raw_id_fields = ("user",)  # Используем raw_id_fields для пользователей


class BudgetInline(admin.TabularInline):
    model = Budget
    extra = 1
    readonly_fields = ("year", "amount")  # Пример readonly_fields


class RiskInline(admin.TabularInline):
    model = Risk
    extra = 1


class ResultInline(admin.TabularInline):
    model = Result
    extra = 1


class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    readonly_fields = ("status",)  # Пример readonly_fields
    filter_horizontal = ("assigned_users",)


@admin.register(Project)
class ProjectAdmin(ImportExportActionModelAdmin, SimpleHistoryAdmin):
    resource_class = ProjectResource
    list_display = (
        "name",
        "client",
        "curator",
        "start_date",
        "end_date",
        "budget_summary",
        "member_count",
    )
    list_filter = ("start_date", "end_date", "client")
    inlines = [
        ProjectMembershipInline,
        BudgetInline,
        RiskInline,
        ResultInline,
        TaskInline,
    ]
    date_hierarchy = "start_date"
    search_fields = ("name", "client", "curator", "description")
    list_display_links = ("name", "client")
    history_list_display = ["name", "client", "curator", "start_date", "end_date"]
    actions = ["export_as_excel"]

    @admin.display(description="Бюджет")
    def budget_summary(self, obj):
        budgets = obj.budgets.all()
        if budgets:
            total = sum(b.amount for b in budgets)
            years = ", ".join(str(b.year) for b in budgets)
            return f"{total} ({years})"
        return "Нет данных"

    @admin.display(description="Участников")
    def member_count(self, obj):
        return (
            obj.members.count()
        )  # Используем прямое обращение к members вместо projectmembership_set


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(SimpleHistoryAdmin):
    list_display = ("user", "project", "role", "is_leader", "date_added")
    list_filter = ("role", "project")
    search_fields = ("user__username", "project__name")
    raw_id_fields = ("user", "project")
    history_list_display = ["user", "project", "role", "date_added"]
    list_display_links = ("user", "project")

    @admin.display(description="Руководитель", boolean=True)
    def is_leader(self, obj):
        return obj.role == "leader"


@admin.register(Budget)
class BudgetAdmin(ImportExportActionModelAdmin, SimpleHistoryAdmin):
    resource_class = BudgetResource
    list_display = ("project", "year", "amount", "formatted_amount")
    list_filter = ("year", "project")
    search_fields = ("project__name",)
    history_list_display = ["project", "year", "amount"]
    actions = ["export_as_excel"]
    list_display_links = ("project", "year")

    @admin.display(description="Сумма")
    def formatted_amount(self, obj):
        return f"${obj.amount:,.2f}"


@admin.register(Risk)
class RiskAdmin(SimpleHistoryAdmin):
    list_display = ("name", "project", "short_description")
    list_filter = ("project",)
    search_fields = ("name", "description", "project__name")
    history_list_display = ["name", "project", "description"]
    list_display_links = ("name", "project")

    @admin.display(description="Описание")
    def short_description(self, obj):
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )


@admin.register(Result)
class ResultAdmin(SimpleHistoryAdmin):
    list_display = ("project", "short_text")
    list_filter = ("project",)
    search_fields = ("text", "project__name")
    history_list_display = ["project", "text"]
    list_display_links = ("project",)

    @admin.display(description="Текст")
    def short_text(self, obj):
        return obj.text[:100] + "..." if len(obj.text) > 100 else obj.text


@admin.register(Task)
class TaskAdmin(ImportExportActionModelAdmin, SimpleHistoryAdmin):
    resource_class = TaskResource
    list_display = (
        "name",
        "project",
        "start_date",
        "end_date",
        "status",
        "duration_days",
    )
    list_filter = ("status", "project", "start_date", "end_date")
    search_fields = ("name", "description", "project__name")
    date_hierarchy = "start_date"
    readonly_fields = ("duration_days",)
    filter_horizontal = ("assigned_users",)
    history_list_display = ["name", "project", "start_date", "end_date", "status"]
    actions = ["export_as_excel"]
    list_display_links = ("name", "project")

    @admin.display(description="Длительность (дни)")
    def duration_days(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None
