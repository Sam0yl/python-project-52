from django.urls import path
from task_manager.tasks import views
from task_manager.tasks.filters import TaskFilter

urlpatterns = [
    path('', views.IndexView.as_view(filterset_class=TaskFilter), name='tasks_list'),
    path('create/', views.TaskCreate.as_view(), name='tasks_create'),
    path('<int:pk>/update/', views.TaskUpdate.as_view(), name='tasks_update'),
    path('<int:pk>/delete/', views.TaskDelete.as_view(), name='tasks_delete'),
    path('<int:pk>/', views.TaskView.as_view(), name='task_views'),
]