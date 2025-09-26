from django.urls import path

from small_web import views

urlpatterns = [
    path("", views.IndexAPI.as_view(), name="index_page"),
    path("signup/", views.SignUpAPI.as_view(), name="signup_page"),
    path("signin/", views.SignInAPI.as_view(), name="signin_page"),
    path("logout/", views.LogOutAPI.as_view(), name="logout_page"),
    path("cash_info/", views.CashDataAPI.as_view(), name="cash_info_page")
]
