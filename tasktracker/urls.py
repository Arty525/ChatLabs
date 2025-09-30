from django.urls import path
from tasktracker.views import TaskCreateAPIView, TaskListAPIView

app_name='tasktracker'

urlpatterns = [
    path('new_task/', TaskCreateAPIView.as_view(), name='new_task'),
    path('tasks_list/', TaskListAPIView.as_view(), name='tasks_list'),
]