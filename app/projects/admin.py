from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)  # Отображаем только поле name
    search_fields = ('name',)  # Добавляем возможность поиска по имени проекта

admin.site.register(Project, ProjectAdmin)