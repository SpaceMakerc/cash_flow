from django.urls import path

from small_web import views

urlpatterns = [
    path("", views.IndexAPI.as_view(), name="index_page"),
    path("signup/", views.SignUpAPI.as_view(), name="signup_page"),
    path("signin/", views.SignInAPI.as_view(), name="signin_page"),
    path("logout/", views.LogOutAPI.as_view(), name="logout_page"),
    path("cash_info/", views.CashDataAPI.as_view(), name="cash_info_page"),
    path("add_cash_flow/", views.add_cash_flow, name="add_cash_flow_page"),
    path("category/", views.categories, name="category"),
    path("subcategory/", views.subcategories, name="subcategory"),
    path(
        "cash_flow_detail/<int:pk>/", views.CashFlowDetailAPI.as_view(),
        name="cash_flow_detail_page"
    ),
    path(
        "delete_cash_flow/<int:pk>/", views.CashFlowDeleteAPI.as_view(),
        name="delete_cash_flow_page"
    ),
    path(
        "change_cash_flow/<int:pk>/", views.change_cash_flow,
        name="change_cash_flow_page"
    )
]
