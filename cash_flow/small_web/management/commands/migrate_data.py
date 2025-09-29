from django.core.management.base import BaseCommand

from small_web.models import (
    CustomUsers,
    Statuses,
    Types,
)


class Command(BaseCommand):
    help = "Добавление информацию в БД"

    def handle(self, *args, **options):
        # Создание CustomUsers
        user = CustomUsers.objects.create_user(
            username="test_user",
            email="test_user@mail.ru",
            password="12345qwerty"  # Пароль для test_user
        )

        # Статусы ДДС
        Statuses.objects.create(
            name="Бизнес", is_common=True, user=user
        )
        Statuses.objects.create(
            name="Личное", is_common=True, user=user
        )
        Statuses.objects.create(
            name="Налог", is_common=True, user=user
        )

        # Типы ДДС

        Types.objects.create(
            name="Пополнение", is_common=True, user=user
        )
        Types.objects.create(
            name="Списание", is_common=True, user=user
        )
