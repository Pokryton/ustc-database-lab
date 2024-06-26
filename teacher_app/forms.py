from django.forms import ModelForm, inlineformset_factory

from .models import *


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ["id", "name", "gender", "title"]


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["id", "name", "hours", "kind"]


class TeacherCourseForm(ModelForm):
    class Meta:
        model = TeacherCourse
        fields = ["teacher", "course", "year", "semester", "hour"]
        labels = {
            "teacher": "教师",
        }


TeacherCourseFormSet = inlineformset_factory(
    Course, TeacherCourse, form=TeacherCourseForm, extra=0
)
