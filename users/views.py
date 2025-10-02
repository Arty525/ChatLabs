from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework import generics


class UserListAPIView(generics.ListAPIView):
    """
    Просмотр списка пользователей, только для супер юзера
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр данных пользователя, только для супер юзера
    """

    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Удалние пользователя, только для супер юзера
    """

    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Изменение данных пользователя, только для супер юзера
    """

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [
        AllowAny,
    ]


class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        AllowAny,
    ]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(self.request.data["password"])
        user.save()
