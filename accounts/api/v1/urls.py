"""
Accounts - API V1 URLs
"""
from django.urls import re_path
from rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
)
from rest_auth.registration.views import (
    RegisterView,
)


urlpatterns = [
    re_path(
        r"^login/$",
        LoginView.as_view(),
        name="rest_login",
    ),
    re_path(
        r"^logout/$",
        LogoutView.as_view(),
        name="rest_logout",
    ),
    re_path(
        r"^user/$",
        UserDetailsView.as_view(),
        name="rest_user_details",
    ),
    re_path(
        r"^change-password/$",
        PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    re_path(
        r"^register/$",
        RegisterView.as_view(),
        name="rest_register",
    ),
]
