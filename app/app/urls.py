"""
URL configuration for messenger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user.views import PasswordResetConfirmView, ActivationView
from projects.views_projects import ProjectListCreateView, ProjectRetrieveUpdateDestroyView
from projects.views_tasks import TaskDetailView, TaskListCreateView
from projects.views_budgets import BudgetDetailView, BudgetListCreateView
from projects.views_results import ResultDetailView, ResultListCreateView
from projects.views_risks import RiskDetailView, RiskListCreateView
from projects.views_add import ProjectLeaderViewSet, ProjectParticipantViewSet
urlpatterns = [
    path('admin/', admin.site.urls),
    path('password_reset/<uid>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('activate/<uid>/<token>/', ActivationView.as_view(), name='activate'),    
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
    path('api/v1/', include('social_django.urls', namespace='social')),
    path('api/v1/projects/', ProjectListCreateView.as_view(), name='project-create'),
    path('api/v1/project/<int:pk>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project-retrieve-update-destroy'),
    path('api/v1/projects/<int:project_id>/tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('api/v1/projects/<int:project_id>/task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/v1/projects/<int:project_id>/budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('api/v1/projects/<int:project_id>/budgets/<int:pk>/', BudgetDetailView.as_view(), name='budget-detail'),
    path('api/v1/projects/<int:project_id>/risks/', RiskListCreateView.as_view(), name='risk-list-create'),
    path('api/v1/projects/<int:project_id>/risks/<int:pk>/', RiskDetailView.as_view(), name='risk-detail'),
    path('api/v1/projects/<int:project_id>/results/', ResultListCreateView.as_view(), name='result-list-create'),
    path('api/v1/projects/<int:project_id>/results/<int:pk>/', ResultDetailView.as_view(), name='result-detail'),
    path('api/v1/projects/<int:pk>/add_leader/', ProjectLeaderViewSet.as_view({'post': 'add_leader'}), name='add-leader'),
    path('api/v1/projects/<int:pk>/add_participant/', ProjectParticipantViewSet.as_view({'post': 'add_participant'}), name='add-participant'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
