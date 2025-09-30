# serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .validators import EmailValidator, FirstNameValidator, LastNameValidator, TelegramIdValidator


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'telegram_id', 'password', 'password_confirm',
                  'is_active', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']
        extra_kwargs = {
            'email': {'validators': [EmailValidator()]},
            'first_name': {'validators': [FirstNameValidator()]},
            'last_name': {'validators': [LastNameValidator()]},
            'telegram_id': {'validators': [TelegramIdValidator()]},
        }

    def validate(self, attrs):
        # Проверка подтверждения пароля при создании или изменении пароля
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)

        if password and password != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)

        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields


class UserUpdateSerializer(UserSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = [field for field in UserSerializer.Meta.fields if field != 'email']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "Пароли не совпадают."})
        return attrs


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