from django import forms
from django.db.models import Q

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
        return Categories.objects.filter(type=types)

    def subcategory_choices(self):
        category = self["category"].value()
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
        label="Статус"
    )
    type = forms.ModelChoiceField(
        queryset=Types.objects.none(),
        label="Тип"
    )
    category = DynamicField(
        forms.ModelChoiceField,
        queryset=category_choices,
        label="Категория"
    )
    subcategory = DynamicField(
        forms.ModelChoiceField,
        queryset=subcategory_choices,
        label="Подкатегория"
    )
    sum = forms.FloatField(
        widget=forms.TextInput(attrs={
            'type': 'number', 'min': '0', "placeholder": "Введите сумму"
        }),
        error_messages={"blank": "Поле Сумма не может быть пустым"},
        label="Сумма",
        required=True
    )
    comment = forms.CharField(
        widget=forms.TextInput(attrs={
            "type": "textarea", "placeholder": "Введите комментарий"
        }),
        label="Комментарий",
        required=False
    )
