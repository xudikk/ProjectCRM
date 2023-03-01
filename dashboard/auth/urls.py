from django.urls import path

from dashboard.auth.auth import sign_in, sign_out, sign_up, otp

urlpatterns = [
    path("", sign_in, name="sign-in"),
    path("regis/", sign_up, name="sign-up"),
    path("otp/", otp, name="otp"),
    path("logout/", sign_out, name="sign-out"),
    path("logout/<conf>/", sign_out, name="sign-out-conf"),
]
