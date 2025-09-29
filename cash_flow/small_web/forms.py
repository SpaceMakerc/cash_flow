from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError

from dynamic_forms import DynamicField, DynamicFormMixin

from small_web.models import Statuses, Types, Categories, SubCategories


class AddCashFlowForm(DynamicFormMixin, forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.common_filter = Q(user=self.user) | Q(user=1)
        super(AddCashFlowForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = Statuses.objects.filter(
            self.common_filter)
        self.fields['status'].initial = Statuses.objects.filter(
            self.common_filter).first()
        self.fields["type"].queryset = Types.objects.filter(
            self.common_filter)
        self.fields["type"].initial = Types.objects.filter(
            self.common_filter).first()

    def category_choices(self):
        types = self["type"].value()
        if types == "":
            return Categories.objects.none()
        return Categories.objects.filter(type=types)

    def subcategory_choices(self):
        category = self["category"].value()
        if category == "":
            return SubCategories.objects.none()
        return SubCategories.objects.filter(category=category)

    created_at = forms.DateField(
        input_formats=['%d.%m.%Y', 'iso-8601'],
        widget=forms.DateInput(attrs={
            "type": "date", "placeholder": "Введите дату в формате дд.мм.гггг"
        }),
        error_messages={"invalid": "Дата должна быть формата дд.мм.гггг"},
        label="Введите дату ДДС",
        required=False
    )
    status = forms.ModelChoiceField(
        queryset=Statuses.objects.none(),
        label="Статус",
        required=False
    )
    type = forms.ModelChoiceField(
        queryset=Types.objects.none(),
        label="Тип",
        required=False
    )
    category = DynamicField(
        forms.ModelChoiceField,
        queryset=category_choices,
        label="Категория",
        required=False
    )
    subcategory = DynamicField(
        forms.ModelChoiceField,
        queryset=subcategory_choices,
        label="Подкатегория",
        required=False
    )
    sum = forms.DecimalField(

        widget=forms.NumberInput(attrs={
            'type': 'number', 'min': '0', "placeholder": "Введите сумму"
        }),
        error_messages={"blank": "Поле Сумма не может быть пустым"},
        label="Сумма",
        required=False
    )
    comment = forms.CharField(
        widget=forms.TextInput(attrs={
            "type": "textarea", "placeholder": "Введите комментарий"
        }),
        label="Комментарий",
        required=False
    )

    def clean(self):
        errors = {}
        super().clean()
        print(self.cleaned_data, '!!!!!!!!!')
        if self.cleaned_data.get("status", None) is None:
            errors["status"] = "Поле Статус не может быть пусты"
        if self.cleaned_data.get("type", None) is None:
            errors["type"] = "Поле Тип не может быть пусты"
        if self.cleaned_data.get("category", None) is None:
            errors["category"] = "Поле Категория не может быть пусты"
        if self.cleaned_data.get("subcategory", None) is None:
            errors["subcategory"] = "Поле Подкатегория не может быть пусты"
        if self.cleaned_data.get("sum", None) is None:
            errors["sum"] = "Поле Сумма не может быть пусты"
        if errors:
            raise ValidationError(errors)


class AddCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.common_filter = Q(user=self.user) | Q(user=1)
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        self.fields["type"].queryset = Types.objects.filter(
            self.common_filter)
        self.fields["type"].initial = Types.objects.filter(
            self.common_filter).first()

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "type": "textarea", "placeholder": "Введите наименование"
        }),
        label="Наименование категории",
        required=False
    )
    type = forms.ModelChoiceField(
        queryset=Types.objects.none(),
        label="Тип категории",
        required=False
    )

    def clean(self):
        errors = {}
        super().clean()
        if not self.cleaned_data.get("name", None):
            errors["name"] = "Поле Наименование категории не может быть пусты"
        if self.cleaned_data.get("type", None) is None:
            errors["type"] = "Выберите поле тип для категории"
        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Categories
        fields = ("name", 'type')
