from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserListAPIView, UserRetrieveAPIView, UserCreateAPIView, \
    UserUpdateAPIView, UserDestroyAPIView

app_name = "users"
urlpatterns = [
    path("", UserListAPIView.as_view(), name="user_list"),  # список всех пользователей
    path(
        "<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"
    ),  # просмотр профиля отдельного пользователя
    path(
        "delete/<int:pk>/", UserDestroyAPIView.as_view(), name="delete_user"
    ),  # удаление пользователя
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # получение токена авторизации
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # обновление токена авторизации
    path(
        "registration/", UserCreateAPIView.as_view(), name="registration"
    ),  # регистрация пользователя
    path(
        "update/<int:pk>", UserUpdateAPIView.as_view(), name="update_user"
    ),  # обновление данных пользователя
]