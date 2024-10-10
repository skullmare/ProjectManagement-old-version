from django.contrib import admin
from .models import Project, Budget, Risk, Result, Task

class BudgetInline(admin.TabularInline):
    model = Budget
    extra = 1

class RiskInline(admin.TabularInline):
    model = Risk
    extra = 1

class ResultInline(admin.TabularInline):
    model = Result
    extra = 1

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'client', 'curator', 'start_date', 'end_date', 'purpose')
    search_fields = ('name', 'client', 'curator')
    inlines = [BudgetInline, RiskInline, ResultInline, TaskInline]

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'year', 'amount')
    search_fields = ('project__name', 'year')

@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'name')
    search_fields = ('project__name', 'name')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id','project',)
    search_fields = ('project__name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','project', 'name', 'status', 'start_date', 'end_date')
    search_fields = ('project__name', 'name')
    list_filter = ('status',)
