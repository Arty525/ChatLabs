from django.urls import path
from rest_framework.routers import DefaultRouter

from tasktracker.views import TaskCreateAPIView, TaskListAPIView, TaskDetailAPIView, TaskUpdateAPIView, \
    TaskDeleteAPIView, CategoryAPIViewset, webhook

app_name='tasktracker'

router = DefaultRouter()
router.register(r"category", CategoryAPIViewset, basename="category")
urlpatterns = [
    path('new_task/', TaskCreateAPIView.as_view(), name='new_task'),
    path('tasks_list/', TaskListAPIView.as_view(), name='tasks_list'),
    #path('tasks_list/<int:telegram_id>/', TaskListAPIView.as_view(), name='tasks_list_tg'),
    path('task_info/<str:pk>/', TaskDetailAPIView.as_view(), name='task_info'),
    path('update_task/<str:pk>/', TaskUpdateAPIView.as_view(), name='update_task'),
    path('delete_task/<str:pk>/', TaskDeleteAPIView.as_view(), name='delete_task'),
    path('webhook/', webhook, name='telegram_webhook')
] + router.urls