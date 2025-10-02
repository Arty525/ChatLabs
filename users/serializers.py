from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .validators import (
    EmailValidator,
    FirstNameValidator,
    LastNameValidator,
    TelegramIdValidator,
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "telegram_id",
            "password",
            "password_confirm",
            "is_active",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["date_joined", "last_login"]
        extra_kwargs = {
            "email": {"validators": [EmailValidator()]},
            "first_name": {"validators": [FirstNameValidator()]},
            "last_name": {"validators": [LastNameValidator()]},
            "telegram_id": {"validators": [TelegramIdValidator()]},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm", None)

        if password and password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        validated_data.pop("password_confirm", None)

        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "telegram_id", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "telegram_id": {"required": False},
        }

    def validate_email(self, value):
        if value == "" or value is None:
            if self.instance:
                return self.instance.email
            raise serializers.ValidationError("Email cannot be empty")
        return value

    def validate(self, attrs):
        attrs = {key: value for key, value in attrs.items() if value is not None and value != ""}
        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            if value is not None and value != "":
                setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "Passwords do not match."}
            )
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        try:
            attrs["username"] = attrs.get(
                "email"
            )
            return super().validate(attrs)
        except Exception:
            raise serializers.ValidationError(
                {"detail": "No active account found with the given credentials"}
            )

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        return token
