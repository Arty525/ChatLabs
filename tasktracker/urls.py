from django.urls import path
from tasktracker.views import TaskCreateAPIView, TaskListAPIView, TaskDetailAPIView, TaskUpdateAPIView, \
    TaskDeleteAPIView

app_name='tasktracker'

urlpatterns = [
    path('new_task/', TaskCreateAPIView.as_view(), name='new_task'),
    path('tasks_list/', TaskListAPIView.as_view(), name='tasks_list'),
    path('task_info/<str:pk>/', TaskDetailAPIView.as_view(), name='task_info'),
    path('update_task/<str:pk>/', TaskUpdateAPIView.as_view(), name='update_task'),
    path('delete_task/<str:pk>/', TaskDeleteAPIView.as_view(), name='delete_task'),
]