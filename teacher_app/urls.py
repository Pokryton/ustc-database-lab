from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),

    path("teacher/", views.teacher_search, name="teacher"),
    path("teacher/add/", views.teacher_add, name="teacher-add"),
]
