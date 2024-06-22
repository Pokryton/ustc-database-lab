from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),

    path("teacher/", views.teacher_search, name="teacher"),
    path("teacher/add/", views.teacher_add, name="teacher-add"),

    path("course/", views.CourseListView.as_view(), name="course"),
    path("course/add/", views.CourseCreateView.as_view(), name="course-add"),
    path("course/<str:pk>", views.CourseDetailView.as_view(), name="course-detail"),
]
