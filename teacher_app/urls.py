from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),

    path("teacher/", views.teacher_search, name="teacher-list"),
    path("teacher/add/", views.teacher_add, name="teacher-add"),
    path("teacher/<str:pk>", views.teacher_detail, name="teacher-detail"),

    path("course/", views.course_list, name="course-list"),
    path("course/add/", views.course_add, name="course-add"),
    path("course/<str:course_id>", views.course_detail, name="course-detail"),
    path("course/update/<str:course_id>", views.course_update, name="course-update"),
    path("course/delete/<str:course_id>", views.course_delete, name="course-delete"),

    path("project/", views.project_list, name="project-list"),
    path("project/add/", views.project_add, name="project-add"),
    path("project/<str:project_id>", views.project_detail, name="project-detail"),
    path("project/update/<str:project_id>", views.project_update, name="project-update"),
    path("project/delete/<str:project_id>", views.project_delete, name="project-delete"),

    path("paper/", views.paper_list, name="paper-list"),
]
