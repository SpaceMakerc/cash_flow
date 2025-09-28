from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.db.models import Q
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from datetime import datetime

from small_web.serializers import (
    SignUpSerializer,
    SignInSerializer,
    ShowCashDataSerializer,
    ChooseCashDataSerializer,
    StatusSerializer,
)
from small_web.models import (
    CashData,
    Statuses,
    SubCategories
)
from small_web.forms import AddCashFlowForm
from small_web.utils.utils_validate import CHOSEN_FIELD
from small_web.utils.utils_create_date_period import create_date_period

# Create your views here.


class IndexAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response(template_name="index.html")


class SignUpAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "signup.html"
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        serializer = SignUpSerializer()
        return Response({"serializer": serializer, "style": self.style})

    def post(self, request):
        user_data = request.POST
        serializer = SignUpSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            messages.add_message(
                request=request, level=messages.SUCCESS,
                message=f"Пользователь {user.username} зарегестрирован"
            )
        else:
            return Response({"serializer": serializer, "style": self.style})
        return redirect(to=reverse("index_page"))


class SignInAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "signin.html"
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        serializer = SignInSerializer()
        return Response({"serializer": serializer, "style": self.style})

    def post(self, request):
        user_data = request.POST
        serializer = SignInSerializer(data=user_data)
        if serializer.is_valid():
            form_info = serializer.validated_data
            user = authenticate(
                request,
                username=form_info["username"],
                password=form_info["password"]
            )
            if user:
                login(request=request, user=user)
                messages.add_message(
                    request=request, level=messages.SUCCESS,
                    message=f"Выполнен вход в систему пользователем "
                            f"{user.username}"
                )
                return redirect(to=reverse("index_page"))
            return Response({
                "serializer": serializer, "style": self.style,
                "not_found": True
            })
        return Response({"serializer": serializer, "style": self.style})


class LogOutAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        logout(request=request)
        return redirect(to=reverse("index_page"))


class CashDataAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cash_data.html"
    permission_classes = [IsAuthenticated]
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        user_id = request.user
        db_info = CashData.objects.filter(user=user_id)
        common_filter = Q(user=request.user) | Q(user=1)
        context = {}
        common_query = SubCategories.objects.select_related(
            'category', 'category__type'
        ).filter(Q(category__user=user_id) | Q(category__user=1))
        statuses_query = Statuses.objects.filter(common_filter)
        context.update({
            "common_query": common_query, "statuses_query": statuses_query
        })
        serializer_choose = ChooseCashDataSerializer()
        serializer_show = ShowCashDataSerializer(db_info, many=True)
        context.update({
            "serializer_show": serializer_show,
            "serializer_choose": serializer_choose,
            "style": self.style
        })
        return Response(context)

    def post(self, request):
        user_data = request.POST
        serializer_check = ChooseCashDataSerializer(data=user_data)
        if serializer_check.is_valid():
            user_id = request.user
            db_info = CashData.objects.filter(user=user_id)
            if any(
                    val != "0" and val != ""
                    for key, val in user_data.items()
                    if key in CHOSEN_FIELD
            ):
                date_range = create_date_period(
                    start_date=user_data.get("created_at_start", None),
                    end_date=user_data.get("created_at_end", None)
                )
                db_info = CashData.objects.filter(
                    Q(user=user_id) & Q(
                        Q(status=user_data.get("status")) |
                        Q(type=user_data.get("type")) |
                        Q(category=user_data.get("category")) |
                        Q(subcategory=user_data.get("subcategory")) |
                        date_range
                    )
                )
            common_filter = Q(user=request.user) | Q(user=1)
            context = {}
            common_query = SubCategories.objects.select_related(
                'category', 'category__type'
            ).filter(Q(category__user=user_id) | Q(category__user=1))
            statuses_query = Statuses.objects.filter(common_filter)
            context.update({
                "common_query": common_query, "statuses_query": statuses_query
            })
            serializer_show = ShowCashDataSerializer(db_info, many=True)
            context.update({
                "serializer_show": serializer_show,
                "serializer_choose": serializer_check,
                "style": self.style
            })
            return Response(context)
        else:
            db_info = CashData.objects.filter(user=request.user)
            serializer_show = ShowCashDataSerializer(db_info, many=True)
            return Response({
                "serializer_show": serializer_show,
                "serializer_choose": serializer_check,
                "style": self.style
            })


@login_required
def add_cash_flow(request):
    if request.method == "GET":
        form = AddCashFlowForm(user=request.user)
        context = {"form": form}
        return render(request, "change_cash_flow_data/add_cashflow.html", context)
    user_data = request.POST
    form = AddCashFlowForm(user_data, user=request.user)
    if form.is_valid():
        cd = form.cleaned_data
        CashData(
            created_at=cd.get("created_at", None),
            status=cd.get("status", None),
            type=cd.get("type", None),
            category=cd.get("category", None),
            subcategory=cd.get("subcategory", None),
            sum=cd.get("sum", None),
            user=request.user,
            comment=cd.get("comment", None)
        ).save()
        return redirect(to=reverse("cash_info_page"))
    context = {"form": form}
    return render(request, "change_cash_flow_data/add_cashflow.html", context)


def categories(request):
    form = AddCashFlowForm(request.GET, user=request.user)
    return HttpResponse(form["category"])


def subcategories(request):
    form = AddCashFlowForm(request.GET, user=request.user)
    return HttpResponse(form["subcategory"])


class CashFlowDetailAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "change_cash_flow_data/detail_cashflow.html"
    permission_classes = [IsAuthenticated]
    style = {'template_pack': 'rest_framework/horizontal/'}

    def get(self, request, pk):
        cash_flow = CashData.objects.get(pk=pk)
        serializer = ShowCashDataSerializer(cash_flow)
        return Response({"serializer": serializer})


class CashFlowDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            cash_flow_row = get_object_or_404(CashData, pk=pk)
            CashData.delete(cash_flow_row)
            return redirect(to=reverse("cash_info_page"))
        except Exception:
            return redirect(
                to=reverse("cash_flow_detail_page", kwargs={"pk": pk})
            )


@login_required
def change_cash_flow(request, pk):
    if request.method == "GET":
        cash_flow_row = get_object_or_404(CashData, pk=pk)
        user_data = model_to_dict(cash_flow_row)
        form = AddCashFlowForm(user_data, user=request.user)
        return render(
            request, "change_cash_flow_data/change_cashflow.html",
            {"form": form}
        )
    user_data = request.POST
    form = AddCashFlowForm(user_data, user=request.user)
    if form.is_valid():
        cd = form.cleaned_data
        CashData(
            id=pk,
            created_at=cd.get("created_at")
            if cd.get("created_at") else datetime.now().date(),
            status=cd.get("status", None),
            type=cd.get("type", None),
            category=cd.get("category", None),
            subcategory=cd.get("subcategory", None),
            sum=cd.get("sum", None),
            user=request.user,
            comment=cd.get("comment", None)
        ).save()
        return redirect(to=reverse("cash_info_page"))
    context = {"form": form}
    return render(
        request, "change_cash_flow_data/change_cashflow.html", context
    )


class StatusesByUserAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "statuses_data.html"
    permission_classes = [IsAuthenticated]
    style = {'template_pack': 'rest_framework/horizontal/'}

    def get(self, request):
        user_id = request.user
        common_filter = Q(user=user_id) | Q(user=1)
        db_info = Statuses.objects.filter(common_filter)
        serializer = StatusSerializer(db_info, many=True)
        context = {"serializer": serializer, "style": self.style}
        return Response(context)


class AddStatusAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "change_statuses_data/add_status.html"
    permission_classes = [IsAuthenticated]
    style = {'template_pack': 'rest_framework/horizontal/'}

    def get(self, request):
        serializer = StatusSerializer()
        return Response({"serializer": serializer, "style": self.style})

    def post(self, request):
        user_data = {
            "user": request.user.id, "name": request.POST.get("name", None)
        }

        serializer = StatusSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return redirect(to=reverse("statuses_info_page"))
        return Response({"serializer": serializer, "style": self.style})


class ChangeStatusAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "change_statuses_data/change_status.html"
    permission_classes = [IsAuthenticated]
    style = {'template_pack': 'rest_framework/horizontal/'}

    def get(self, request, pk):
        status_row = get_object_or_404(Statuses, pk=pk)
        serializer = StatusSerializer(status_row)
        return Response({"serializer": serializer, "style": self.style})

    def post(self, request, pk):
        user_data = {
            "user": request.user.id, "name": request.POST.get("name", None)
        }
        serializer = StatusSerializer(data=user_data)
        if serializer.is_valid():
            Statuses(
                id=pk,
                user=serializer.validated_data.get("user"),
                name=serializer.validated_data.get("name")
            ).save()
            return redirect(to=reverse("statuses_info_page"))
        return Response({"serializer": serializer, "style": self.style})


class DeleteStatusAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            status_row = get_object_or_404(Statuses, pk=pk)
            Statuses.delete(status_row)
            return redirect(to=reverse("statuses_info_page"))
        except Exception:
            return redirect(to=reverse("statuses_info_page"))
