from django.contrib import admin
from .models import Project, ProjectMembership, Budget, Risk, Result, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'curator', 'start_date', 'end_date')
    search_fields = ('name', 'client')
    list_filter = ('start_date', 'end_date')

@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')
    search_fields = ('user__username', 'project__name')
    
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('project', 'year', 'amount')
    search_fields = ('project__name',)
    list_filter = ('year',)

@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('project', 'name')
    search_fields = ('project__name', 'name')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('project',)
    search_fields = ('project__name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'start_date', 'end_date', 'status')
    search_fields = ('name', 'project__name')
    list_filter = ('status', 'start_date', 'end_date')
