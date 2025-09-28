from rest_framework import serializers

from small_web.models import CustomUsers, CashData, Statuses
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


class ShowCashDataSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(
        format="%d.%m.%Y", input_formats=['%d.%m.%Y', 'iso-8601'],
        style={"placeholder": "Введите дату в формате дд.мм.гггг"}
    )
    status = serializers.CharField(source="status.name")
    type = serializers.CharField(source="type.name")
    category = serializers.CharField(source="category.name")
    subcategory = serializers.CharField(source="subcategory.name")

    class Meta:
        model = CashData
        fields = (
            "id", "created_at", "status", "type", "category",
            "subcategory", "sum", "comment",
        )


class ChooseCashDataSerializer(serializers.ModelSerializer):
    created_at_start = serializers.DateField(
        format="%d.%m.%Y", input_formats=['%d.%m.%Y', 'iso-8601'],
        style={"placeholder": "Введите дату в формате дд.мм.гггг"},
        allow_null=True,
        label="Выберите начало периода",
        error_messages={"invalid": "Дата должна быть формата дд.мм.гггг"}
    )
    created_at_end = serializers.DateField(
        format="%d.%m.%Y", input_formats=['%d.%m.%Y', 'iso-8601'],
        style={"placeholder": "Введите дату в формате дд.мм.гггг"},
        allow_null=True,
        label="Выберите окончание периода",
        error_messages={"invalid": "Дата должна быть формата дд.мм.гггг"}
    )
    status = serializers.CharField(allow_null=True, required=False)
    type = serializers.CharField(allow_null=True, required=False)
    category = serializers.CharField(allow_null=True, required=False)
    subcategory = serializers.CharField(allow_null=True, required=False)
    sum = serializers.FloatField(allow_null=True, required=False)

    class Meta:
        model = CashData
        fields = (
            "status", "type", "category", "subcategory",
            "sum", "comment", "created_at_start", "created_at_end"
        )


class StatusSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        allow_null=False, required=True,
        error_messages={"blank": "Поле Наименование не может быть пустым"},
        label="Наименование"
    )

    class Meta:
        model = Statuses
        fields = ("id", "name", "user")
