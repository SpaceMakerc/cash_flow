from rest_framework import serializers

from small_web.models import CustomUsers, CashData
from small_web.utils.utils_validate import (
    username_validation_on_creating,
    email_validation_on_creating,
)


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password", "placeholder": "Введите пароль"},
        error_messages={"blank": "Поле Пароль не может быть пустым"},
        label="Пароль",
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
        user = CustomUsers(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        user.set_password(raw_password=validated_data["password"])
        user.save()
        return user

    class Meta:
        model = CustomUsers
        fields = ("username", "email", "password", "password2")


class SignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        style={"placeholder": "Введите логин"},
        error_messages={"blank": "Поле Логин не может быть пустым"},
        label="Логин",
    )
    password = serializers.CharField(
        style={"input_type": "password", "placeholder": "Введите пароль"},
        error_messages={"blank": "Поле Пароль не может быть пустым"},
        label="Пароль"
    )

    class Meta:
        model = CustomUsers
        fields = ("username", "password")


class GetCashDataSerializer(serializers.Serializer):
    created_at = serializers.DateField()
    status = serializers.CharField()
    type = serializers.CharField()
    category = serializers.CharField()
    subcategory = serializers.CharField()
    sum = serializers.FloatField()
    comment = serializers.CharField()
