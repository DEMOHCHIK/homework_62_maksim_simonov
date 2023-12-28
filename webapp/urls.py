from django.urls import path
from webapp.views import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, \
    TaskDetailView, TaskCreateView, TaskDeleteView, TaskUpdateView

app_name = 'webapp'

urlpatterns = [
    path('', ProjectListView.as_view()),
    path('projects/', ProjectListView.as_view(), name='home'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/create/', ProjectCreateView.as_view(), name='add_project'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/<int:pk>/tasks/add/', TaskCreateView.as_view(), name='add_task'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:project_pk>/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail')
]
