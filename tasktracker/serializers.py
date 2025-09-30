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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Указываем, что используем email вместо username

    def validate(self, attrs):
        # Пробуем аутентифицировать с email
        try:
            attrs['username'] = attrs.get('email')  # Добавляем username для совместимости
            return super().validate(attrs)
        except Exception as e:
            raise serializers.ValidationError({
                'detail': 'No active account found with the given credentials'
            })

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем кастомные claims в токен
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token