from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.db.models import Q


from small_web.serializers import (
    SignUpSerializer,
    SignInSerializer,
    ShowCashDataSerializer,
    ChooseCashDataSerializer
)
from small_web.models import (
    CashData,
    Statuses,
    SubCategories
)
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
                    Q(status=user_data.get("status", None)) |
                    Q(type=user_data.get("type", None)) |
                    Q(category=user_data.get("category", None)) |
                    Q(subcategory=user_data.get("subcategory", None))
                    | date_range if date_range else ~Q(created_at_start=None)
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
