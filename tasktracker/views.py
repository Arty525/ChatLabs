from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from tasktracker.models import Task
from tasktracker.serializers import TaskSerializer


# Create your views here.
class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)