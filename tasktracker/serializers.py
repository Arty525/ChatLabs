from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from tasktracker.models import Task, Category
from tasktracker.validators import TaskDeadlineValidator

class TaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(input_formats=['%d.%m.%Y %H:%M'], )
    class Meta:
        model = Task
        fields = '__all__'
        validators = [TaskDeadlineValidator(deadline='deadline',),]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
