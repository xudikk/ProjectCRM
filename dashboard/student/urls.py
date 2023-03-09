from django.urls import path
from .views import *

urlpatterns = [
    path('change/', new, name="student-new"),
    path('', st_index, name="student-index"),
    path('profile/', st_profile, name="student-profile"),
]


