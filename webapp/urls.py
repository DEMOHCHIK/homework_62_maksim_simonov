from django.urls import path
from webapp.views import TaskListView, TaskDetailView, TaskAddView, TaskDeleteView, TaskEditView

urlpatterns = [
    path('', TaskListView.as_view()),
    path('tasks/', TaskListView.as_view(), name='home'),
    path('tasks/create/', TaskAddView.as_view(), name='add-task'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<int:pk>/edit/', TaskEditView.as_view(), name='task-edit'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail')
]
