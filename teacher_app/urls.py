from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),

    path("teacher/", views.teacher_search, name="teacher"),
    path("teacher/add/", views.teacher_add, name="teacher-add"),
    path("teacher/<str:pk>", views.teacher_detail, name="teacher-detail"),

    path("course/", views.course_list, name="course"),
    path("course/add/", views.course_create, name="course-add"),
    path("course/<str:pk>", views.CourseDetailView.as_view(), name="course-detail"),
    path("course/delete/<str:pk>", views.CourseDeleteView.as_view(), name="course-delete"),
    path("course/update/<str:course_id>", views.course_update, name="course-update"),
]
