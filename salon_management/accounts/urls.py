from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "customer/login/",
        views.phone_login,
        name="phone_login"
    ),

    path(
        "customer/verify-otp/",
        views.verify_otp,
        name="verify_otp"
    ),

    path(
        "customer/resend-otp/",
        views.resend_otp,
        name="resend_otp"
    ),

    path(
        "customer/complete-profile/",
        views.complete_profile,
        name="complete_profile"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),
]