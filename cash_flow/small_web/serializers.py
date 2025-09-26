from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from small_web.models import CustomUsers
from small_web.utils.utils_validate import (
    username_validation_on_creating,
    email_validation_on_creating,
)


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password", "placeholder": "Введите пароль"},
        error_messages={"blank": "Поле Пароль не может быть пустым"},
        label="Пароль"
    )
    password2 = serializers.CharField(
        style={"input_type": "password", "placeholder": "Повторите пароль"},
        error_messages={"blank": "Поле Пароль не может быть пустым"},
        label="Пароль",
    )
    email = serializers.EmailField(
        style={"placeholder": "Введите email"},
        error_messages={"blank": "Поле Почта не может быть пустым"},
        label="Почта",
    )
    username = serializers.CharField(
        style={"placeholder": "Введите логин"},
        error_messages={"blank": "Поле Логин не может быть пустым"},
        label="Логин",
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password": "Значения паролей должны быть одинаковыми"
            })
        existed_username = username_validation_on_creating(attrs["username"])
        if existed_username:
            raise serializers.ValidationError({
                "username": "Пользователь с таким логином уже существует"
            })
        existed_email = email_validation_on_creating(attrs["email"])
        if existed_email:
            raise serializers.ValidationError({
                "email": "Пользователь с такой почтой уже существует"
            })

        return attrs

    def create(self, validated_data) -> CustomUsers:
        validated_data["password"] = make_password(validated_data["password"])
        user = CustomUsers.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        return user

    class Meta:
        model = CustomUsers
        fields = ("username", "email", "password", "password2")
