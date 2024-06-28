from django import forms

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
        exclude = ["teachers"]


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

        if not actual_hours:
            raise ValidationError("请添加授课信息")

        for year, semester in actual_hours:
            hours = actual_hours[year, semester]
            if hours != expected_hours:
                semester_name = TeacherCourse.SEMESTER_CHOICES[semester]
                raise ValidationError(
                    f"{year} 年{semester_name}授课总学时 ({hours}) 与课程学时 ({expected_hours}) 不匹配"
                )


TeacherCourseFormSet = inlineformset_factory(
    Course,
    TeacherCourse,
    fields="__all__",
    max_num=1,
    formset=BaseTeacherCourseFormSet,
)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ["teachers"]


class BaseTeacherProjectFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        if not hasattr(self.instance, "total_fund"):
            raise ValidationError("未指定项目总经费")

        expected_fund = self.instance.total_fund
        actual_fund = 0

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            cleaned_data = form.clean()
            if not cleaned_data:
                continue

            actual_fund += cleaned_data["fund"]

        if actual_fund != expected_fund:
            raise ValidationError(
                f"教师承担经费总额 (${actual_fund}) 与项目总经费 (${expected_fund}) 不匹配"
            )


TeacherProjectFormSet = inlineformset_factory(
    Project,
    TeacherProject,
    fields="__all__",
    max_num=1,
    formset=BaseTeacherProjectFormSet,
)


class PaperForm(ModelForm):
    class Meta:
        model = Paper
        exclude = ["teachers"]


class BaseTeacherPaperFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        has_corresp = False

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            cleaned_data = form.clean()
            if not cleaned_data:
                continue

            if has_corresp and cleaned_data["corresp"]:
                raise ValidationError("一篇论文只能有一位通讯作者")

            has_corresp |= cleaned_data["corresp"]

        if not has_corresp:
            raise ValidationError("请指定通讯作者")


TeacherPaperFormSet = inlineformset_factory(
    Paper,
    TeacherPaper,
    fields="__all__",
    max_num=1,
    formset=BaseTeacherPaperFormSet,
)


class YearRangeForm(forms.Form):
    start_year = forms.IntegerField(label="开始年份")
    end_year = forms.IntegerField(label="结束年份")
