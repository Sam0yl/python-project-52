from django.urls import path
from task_manager.labels import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='labels_list'),
    path('create/', views.LabelCreate.as_view(), name='labels_create'),
    path('<int:pk>/update/', views.LabelUpdate.as_view(), name='labels_update'),
    path('<int:pk>/delete/', views.LabelDelete.as_view(), name='labels_delete'),
]
