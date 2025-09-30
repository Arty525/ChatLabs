from django.urls import path
from tasktracker.views import TaskCreateAPIView

app_name='tasktracker'

urlpatterns = [
    path('new_task/', TaskCreateAPIView.as_view(), name='new_task'),
]