from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import generics, status


class UserListAPIView(generics.ListAPIView):
    """
    Просмотр списка пользователей, только для супер юзера
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Просмотр данных пользователя, только для супер юзера
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Удалние пользователя, только для супер юзера
    """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Изменение данных пользователя, только для супер юзера
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(generics.CreateAPIView):
    """
    Регистрация пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(self.request.data["password"])
        user.save()