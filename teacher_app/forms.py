from django.forms import (
    ModelForm,
    BaseInlineFormSet,
    ValidationError,
    inlineformset_factory,
)

from .models import *


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ["id", "name", "gender", "title"]


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ["id", "name", "total_hours", "kind"]


class TeacherCourseForm(ModelForm):
    class Meta:
        model = TeacherCourse
        fields = ["teacher", "course", "year", "semester", "hours"]
        labels = {
            "teacher": "教师",
        }


class BaseTeacherCourseFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        if not hasattr(self.instance, "total_hours"):
            raise ValidationError("未指定课程总学时")

        expected_hours = self.instance.total_hours
        actual_hours = {}

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            cleaned_data = form.clean()
            if not cleaned_data:
                continue

            year = cleaned_data["year"]
            semester = cleaned_data["semester"]

            if (year, semester) not in actual_hours:
                actual_hours[year, semester] = 0

            actual_hours[year, semester] += cleaned_data["hours"]

        for year, semester in actual_hours:
            hours = actual_hours[year, semester]
            if hours != expected_hours:
                semester_name = TeacherCourse.SEMESTER_CHOICES[semester]
                raise ValidationError(
                    f"{year} 年{semester_name}授课总学时与课程学时不匹配"
                )


TeacherCourseFormSet = inlineformset_factory(
    Course,
    TeacherCourse,
    form=TeacherCourseForm,
    extra=0,
    formset=BaseTeacherCourseFormSet,
)
