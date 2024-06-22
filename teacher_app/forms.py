from django.forms import ModelForm, inlineformset_factory

from .models import Teacher, Course, TeacherCourse

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ["id", "name", "gender", "title"]

class TeacherCourseForm(ModelForm):
    class Meta:
        model = TeacherCourse
        fields = ["teacher", "course", "year", "semester", "hour"]
        labels = {
            "teacher":  "教师",
        }


TeacherCourseFormSet = inlineformset_factory(Course, TeacherCourse, form=TeacherCourseForm, extra=1)


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["id", "name", "hours", "kind"]
        labels = {
            "id":  "课程号",
            "name": "课程名称",
            "hours": "学时数",
            "kind": "课程性质",
        }
        inlines = [TeacherCourseFormSet]
