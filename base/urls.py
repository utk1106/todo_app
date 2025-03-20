# from django.urls import path
# from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
# from django.contrib.auth.views import LogoutView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# urlpatterns = [
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
#     path('register/', RegisterPage.as_view(), name='register'),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get JWT
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT

#     path('', TaskList.as_view(), name='tasks'),
#     path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
#     path('task-create/', TaskCreate.as_view(), name='task-create'),
#     path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
#     path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
# ]
#api endpoint
from django.urls import path
from .views import (
    LogoutAPI, TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage,
    TaskListAPI, TaskDetailAPI, TaskCreateAPI, TaskUpdateAPI, TaskDeleteAPI
)
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/logout/', LogoutAPI.as_view(), name='api-logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    # API endpoints
    path('api/tasks/', TaskListAPI.as_view(), name='api-tasks'),
    path('api/task/<int:pk>/', TaskDetailAPI.as_view(), name='api-task-detail'),
    path('api/task-create/', TaskCreateAPI.as_view(), name='api-task-create'),
    path('api/task-update/<int:pk>/', TaskUpdateAPI.as_view(), name='api-task-update'),
    path('api/task-delete/<int:pk>/', TaskDeleteAPI.as_view(), name='api-task-delete'),
]