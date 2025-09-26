from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUsers(AbstractUser):

    username = models.CharField(
        max_length=150, verbose_name="Логин", unique=True
    )
    email = models.EmailField(verbose_name="Почта")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "custom_users"


class Status(models.Model):
    user = models.ForeignKey(
        "CustomUsers", related_name="user_status", on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    is_common = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        db_table = "flow_status"
