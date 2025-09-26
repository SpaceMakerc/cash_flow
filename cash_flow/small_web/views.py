from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, reverse

from small_web.serializers import (
    SignUpSerializer,
    SignInSerializer,
    GetCashDataSerializer,
)
from small_web.models import CashData

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

    def get(self, request):
        db_info = CashData.objects.select_related(
            'status', 'type', 'category', 'subcategory'
        ).only(
            'created_at', 'status', 'type', 'category',
            'subcategory', 'sum', 'comment'
        ).filter(user=request.user.id)
        serializer = GetCashDataSerializer(db_info, many=True)
        return Response({"serializer": serializer})
