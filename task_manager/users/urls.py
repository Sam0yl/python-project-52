from django.urls import path
from task_manager.users import views
from django.views.i18n import set_language

urlpatterns = [
    path('', views.IndexView.as_view(), name='users_list'),
    path('create/', views.UserCreate.as_view(), name='users_create'),
    path('<int:pk>/update/', views.UserUpdate.as_view(), name='users_update'),
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='users_delete'),
]