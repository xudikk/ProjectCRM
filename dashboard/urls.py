from django.urls import path, include

from .views import index

urlpatterns = [
    path("", index, name='home'),
    path('member/st/', include('dashboard.student.urls')),
    path('auth/', include('dashboard.auth.urls'))
]
