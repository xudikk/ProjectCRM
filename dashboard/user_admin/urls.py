from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="admin-home"),
    path("gr/", manage_group, name="admin-group"),
    path("gr/<int:group_id>/", manage_group, name="admin-group-one"),

    path("mentor/", manage_mentor, name="admin-mentor"),
    path("one/<int:_id>/", manage_mentor, name="admin-member-one"),
    path("edit/<int:edit_id>/", manage_mentor, name="admin-member-edit"),


    path("student/", manege_student, name="admin-student"),
    path("ins/", interested, name="admin-interested"),
    path("ins/<int:contac_id>", interested, name="admin-interested-contacted"),
    path("ins/detail/<int:pk>/", interested, name="admin-inters-detail"),

]

