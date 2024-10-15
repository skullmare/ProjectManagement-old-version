from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user.views import PasswordResetConfirmView, ActivationView
from projects.views import (
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    BudgetListView,
    BudgetCreateView,
    BudgetDetailView,
    ResultListView,
    ResultCreateView,
    ResultDetailView,
    RiskListView,
    RiskCreateView,
    RiskDetailView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('password_reset/<uid>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('activate/<uid>/<token>/', ActivationView.as_view(), name='activate'),    
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/', include('social_django.urls', namespace='social')),
    
    # URL-ы для управления проектами
    path('api/v1/projects/', ProjectListView.as_view(), name='project-list'),  # Список проектов
    path('api/v1/projects/create/', ProjectCreateView.as_view(), name='project-create'),  # Создание проекта
    path('api/v1/projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),  # Получение проекта
    path('api/v1/projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),  # Обновление проекта
    path('api/v1/projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),  # Удаление проекта

    # # URL-ы для управления задачами
    path('api/v1/projects/<int:project_id>/tasks/', TaskListView.as_view(), name='task-list'),  # Список задач
    path('api/v1/projects/<int:project_id>/tasks/create/', TaskCreateView.as_view(), name='task-create'),  # Создание задачи
    path('api/v1/projects/<int:project_id>/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),  # Получение задачи

    # URL-ы для управления бюджетами
    path('api/v1/projects/<int:project_id>/budgets/', BudgetListView.as_view(), name='budget-list'),  # Список бюджетов
    path('api/v1/projects/<int:project_id>/budgets/create/', BudgetCreateView.as_view(), name='budget-create'),  # Создание бюджета
    path('api/v1/projects/<int:project_id>/budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),  # Получение бюджета

    # URL-ы для управления результатами
    path('api/v1/projects/<int:project_id>/results/', ResultListView.as_view(), name='result-list'),  # Список результатов
    path('api/v1/projects/<int:project_id>/results/create/', ResultCreateView.as_view(), name='result-create'),  # Создание результата
    path('api/v1/projects/<int:project_id>/results/<int:pk>/', ResultDetailView.as_view(), name='result-detail'),  # Получение результата

    # URL-ы для управления рисками
    path('api/v1/projects/<int:project_id>/risks/', RiskListView.as_view(), name='risk-list'),  # Список рисков
    path('api/v1/projects/<int:project_id>/risks/create/', RiskCreateView.as_view(), name='risk-create'),  # Создание риска
    path('api/v1/projects/<int:project_id>/risks/<int:pk>/', RiskDetailView.as_view(), name='risk-detail'),  # Получение риска
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
