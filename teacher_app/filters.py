import django_filters

from .models import *


class CourseFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr="icontains", label="课程号")
    name = django_filters.CharFilter(lookup_expr="icontains", label="课程名")
    teacher__name = django_filters.CharFilter(
        field_name="teachers", lookup_expr="name__icontains", label="教师姓名"
    )
    semester = django_filters.ChoiceFilter(
        choices=TeacherCourse.SEMESTER_CHOICES,
        field_name="teachercourse",
        lookup_expr="semester__icontains",
        label="开课学期",
    )

    class Meta:
        model = Course
        fields = ["id", "name", "kind"]
