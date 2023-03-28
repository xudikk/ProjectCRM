from django.urls import path
from .views import *


urlpatterns = [
    path("", home, name="admin-home"),

    # group
    path("gr/", manage_group, name="admin-group"),
    path("gr/list/<int:status>/", manage_group, name="admin-group-list"),
    path("gr/<int:group_id>/", manage_group, name="admin-group-one"),
    path("gr/edit/<int:_id>/", manage_group, name="admin-group-edit"),
    path("gr/<int:group_id>/student/<int:student_id>/", manage_group, name="admin-group-del-student"),
    path("gr/<int:group_id>/gs/<int:status>", manage_group, name="admin-group-add-student"),

    # course
    path("course/", manage_course, name="admin-course"),
    path("course/one/<int:pk>/", manage_course, name="admin-course-one"),
    path("course/<int:edit_id>/", manage_course, name="admin-course-edit"),

    # member
    path("mentor/", manage_mentor, name="admin-mentor"),
    path("one/<int:_id>/", manage_mentor, name="admin-member-one"),
    path("edit/<int:edit_id>/", manage_mentor, name="admin-member-edit"),
    path("student/", manege_student, name="admin-student"),

    # interesting
    path("ins/", interested, name="admin-interested"),
    path("ins/<int:contac_id>", interested, name="admin-interested-contacted"),
    path("ins/detail/<int:pk>/", interested, name="admin-inters-detail"),

    # settings
    path('chp/', change_pass, name="admin-change-pass")

]

