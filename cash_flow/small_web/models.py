from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUsers(AbstractUser):
    """
    Таблица кастомного пользователя для входа в систему и просмотра своих данных
    по движению денежных средств
    В таблице изначально есть базовый пользователь у которого есть общие типы и
    статусы - base_user
    """

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


class Statuses(models.Model):
    """
    Таблица статусов двежения денежных средств. В таблице есть ссылка на
    пользователей, чтобы каждый пользователь мог добавлять свои статусы и только
    он мог их видеть (включая статусы базового пользователя)
    """
    user = models.ForeignKey(
        "CustomUsers", related_name="user_status", on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    is_common = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        db_table = "flow_status"


class Types(models.Model):
    """
    Таблица типов движения денежных средств. В таблице есть ссылка на
    пользователей, чтобы каждый пользователь мог добавлять свои типы и только он
    мог их видеть (включая статусы базового пользователя)
    """
    user = models.ForeignKey(
        "CustomUsers", related_name="user_types", on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    is_common = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        db_table = "flow_types"


class Categories(models.Model):
    """
    Таблица категорий движения денежных средств. В таблице есть ссылка на
    пользователей, чтобы каждый пользователь мог добавлять свои категории и
    только он мог их видеть (включая статусы базового пользователя)
    """
    user = models.ForeignKey(
        "CustomUsers", related_name="user_categories", on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        "Types", related_name="type_categories", on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "flow_categories"


class SubCategories(models.Model):
    """
    Таблица подкатегорий движения денежных средств
    """
    category = models.ForeignKey(
        "Categories", related_name="subcategories", on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        db_table = "subcategories"


class CashData(models.Model):
    """
    Таблица с общей информацией о движении денежных средств
    """
    created_at = models.DateField(
        auto_now_add=True, verbose_name="Дата создания записи", null=False
    )
    status = models.ForeignKey(
        "Statuses", related_name="cash_statuses", on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        "Types", related_name="cash_types", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "Categories", related_name="cash_categories", on_delete=models.CASCADE
    )
    subcategory = models.ForeignKey(
        "SubCategories", related_name="cash_subcategories",
        on_delete=models.CASCADE
    )
    sum = models.DecimalField(
        null=False, verbose_name="Сумма", max_digits=10, decimal_places=3
    )
    user = models.ForeignKey(
        "CustomUsers", related_name="user_cash_data", on_delete=models.CASCADE
    )
    comment = models.TextField(
        null=True, blank=True, verbose_name="Комментарий"
    )

    class Meta:
        db_table = "cash_data"
