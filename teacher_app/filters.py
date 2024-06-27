import django_filters

from .models import *


class CourseFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr="icontains", label="课程号")
    name = django_filters.CharFilter(lookup_expr="icontains", label="课程名称")
    teacher__name = django_filters.CharFilter(
        field_name="teachers", lookup_expr="name__icontains", label="授课教师姓名"
    )
    semester = django_filters.ChoiceFilter(
        choices=TeacherCourse.SEMESTER_CHOICES,
        field_name="teachercourse",
        lookup_expr="semester",
        label="开课学期",
    )

    class Meta:
        model = Course
        fields = ["id", "name", "kind"]



class ProjectFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr="icontains", label="项目号")
    name = django_filters.CharFilter(lookup_expr="icontains", label="项目名称")
    source = django_filters.CharFilter(lookup_expr="icontains", label="项目来源")
    teacher__name = django_filters.CharFilter(
        field_name="teachers", lookup_expr="name__icontains", label="承担教师姓名"
    )

    class Meta:
        model = Project
        fields = ["id", "name", "source", "kind"]


class PaperFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr="icontains", label="论文号")
    title = django_filters.CharFilter(lookup_expr="icontains", label="论文名称")
    source = django_filters.CharFilter(lookup_expr="icontains", label="发表源")
    teacher__name = django_filters.CharFilter(
        field_name="teachers", lookup_expr="name__icontains", label="作者姓名"
    )

    class Meta:
        model = Paper
        fields = ["id", "title", "source", "kind", "level"]
