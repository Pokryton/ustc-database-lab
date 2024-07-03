from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),

    path("teacher/", views.teacher_list, name="teacher-list"),
    path("teacher/add/", views.teacher_add, name="teacher-add"),
    path("teacher/<str:pk>/summary/", views.teacher_summary, name="teacher-summary"),
    path("teacher/<str:pk>/update/", views.teacher_update, name="teacher-update"),
    path("teacher/<str:pk>/delete/", views.teacher_delete, name="teacher-delete"),

    path("course/", views.course_list, name="course-list"),
    path("course/add/", views.CourseCreateView.as_view(), name="course-add"),
    path("course/<str:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("course/<str:pk>/", views.course_detail, name="course-detail"),
    path("course/<str:pk>/delete/", views.course_delete, name="course-delete"),

    path("project/", views.project_list, name="project-list"),
    path("project/add/", views.ProjectCreateView.as_view(), name="project-add"),
    path("project/<str:pk>/update/", views.ProjectUpdateView.as_view(), name="project-update"),
    path("project/<str:pk>/", views.project_detail, name="project-detail"),
    path("project/<str:pk>/delete/", views.project_delete, name="project-delete"),

    path("paper/", views.paper_list, name="paper-list"),
    path("paper/add/", views.PaperCreateView.as_view(), name="paper-add"),
    path("paper/<str:pk>/update/", views.PaperUpdateView.as_view(), name="paper-update"),
    path("paper/<str:pk>/", views.paper_detail, name="paper-detail"),
    path("paper/<str:pk>/delete/", views.paper_delete, name="paper-delete"),
]
