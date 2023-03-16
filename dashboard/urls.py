from django.urls import path, include

from .views import index, enroll

urlpatterns = [
    path("", index, name='home'),
    path('member/st/', include('dashboard.student.urls')),
    path('member/admin/', include('dashboard.user_admin.urls')),
    path('auth/', include('dashboard.auth.urls')),
    path("enroll/", enroll, name="enroll")
]
