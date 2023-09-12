from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='tasks_list'),
    path('create/', views.TaskCreate.as_view(), name='tasks_create'),
    path('<int:pk>/update/', views.TaskUpdate.as_view(), name='tasks_update'),
    path('<int:pk>/delete/', views.TaskDelete.as_view(), name='tasks_delete'),
]