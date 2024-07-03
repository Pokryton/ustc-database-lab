from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db.models import ProtectedError
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import *
from .filters import *


def index(request):
    return redirect("teacher-list")


def teacher_list(request):
    filter = TeacherFilter(request.GET or None, queryset=Teacher.objects.all())
    teacher_list = filter.qs
    context = {"filter": filter, "teacher_list": teacher_list}
    return render(request, "teacher_app/teacher_list.html", context)


def teacher_add(request):
    form = TeacherForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f"教师 {teacher.name} 登记成功！")
            return redirect("teacher-list")

    context = {"form": form}
    return render(request, "teacher_app/teacher_form.html", context)


def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, instance=teacher)
    form.fields["id"].disabled = True

    if request.method == "POST":
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f"教师 {teacher.name} 更新成功！")
            return redirect("teacher-list")

    context = {"form": form}
    return render(request, "teacher_app/teacher_form.html", context)


@require_http_methods(["POST"])
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    try:
        s = str(teacher)
        teacher.delete()
        messages.success(request, f"教师 {s} 删除成功！")
    except ProtectedError:
        messages.error(request, f"无法删除教师 {teacher}：存在关联数据")

    return redirect("teacher-list")


def teacher_summary(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = YearRangeForm(request.GET or None)
    context = {"teacher": teacher}

    if request.GET:
        form = YearRangeForm(request.GET)
        if form.is_valid():
            start_year = form.cleaned_data["start_year"]
            end_year = form.cleaned_data["end_year"]

            teachercourse_list = TeacherCourse.objects.filter(
                Q(teacher=teacher),
                Q(year__gte=start_year),
                Q(year__lte=end_year),
            )

            teacherpaper_list = TeacherPaper.objects.filter(
                Q(teacher=teacher),
                Q(paper__pub_year__gte=start_year),
                Q(paper__pub_year__lte=end_year),
            )

            teacherproject_list = TeacherProject.objects.filter(
                Q(teacher=teacher),
                Q(project__start_year__lte=end_year),
                Q(project__end_year__gte=start_year),
            )

            context.update(
                {
                    "start_year": start_year,
                    "end_year": end_year,
                    "teachercourse_list": teachercourse_list,
                    "teacherpaper_list": teacherpaper_list,
                    "teacherproject_list": teacherproject_list,
                }
            )

    context["form"] = form
    return render(request, "teacher_app/teacher_summary.html", context)


def course_list(request):
    filter = CourseFilter(request.GET or None, queryset=Course.objects.all())
    course_list = filter.qs.distinct()
    context = {"filter": filter, "course_list": course_list}

    return render(request, "teacher_app/course_list.html", context)


class CreateWithInlinesView(View):
    model = None
    form_class = None
    formset_class = None
    template_name = "teacher_app/form_with_inlines.html"
    success_redirect = None

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        formset = self.formset_class()
        context = {
            "model_name": self.model._meta.verbose_name,
            "form": form,
            "formset": formset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = self.formset_class(request.POST)

        model_name = self.model._meta.verbose_name

        if form.is_valid():
            object = form.save(commit=False)
            formset.instance = object

            if formset.is_valid():
                object.save()
                formset.save()
                messages.success(request, f"{model_name} {object} 登记成功！")
                return redirect(self.success_redirect)

        context = {
            "model_name": model_name,
            "form": form,
            "formset": formset
        }
        return render(request, self.template_name, context)


class UpdateWithInlinesView(View):
    model = None
    form_class = None
    formset_class = None
    template_name = "teacher_app/form_with_inlines.html"
    success_redirect = None

    def get(self, request, *args, **kwargs):
        object = get_object_or_404(self.model, pk=kwargs.get("pk"))
        form = self.form_class(instance=object)
        form.fields["id"].disabled = True
        formset = self.formset_class(instance=object)

        context = {
            "model_name": self.model._meta.verbose_name,
            "form": form,
            "formset": formset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        object = get_object_or_404(self.model, pk=kwargs.get("pk"))
        form = CourseForm(request.POST, instance=object)
        form.fields["id"].disabled = True
        formset = TeacherCourseFormSet(request.POST, instance=object)

        model_name = self.model._meta.verbose_name

        if form.is_valid() and formset.is_valid():
            formset.instance = form.save()
            formset.save()
            messages.success(request, f"{model_name} {object} 更新成功！")
            return redirect(self.success_redirect)

        context = {
            "model_name": model_name,
            "form": form,
            "formset": formset,
        }
        return render(request, "teacher_app/form_with_inlines.html", context)


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {"course": course}
    return render(request, "teacher_app/course_detail.html", context)


class CourseCreateView(CreateWithInlinesView):
    model = Course
    form_class = CourseForm
    formset_class = TeacherCourseFormSet
    success_redirect = "course-list"


class CourseUpdateView(UpdateWithInlinesView):
    model = Course
    form_class = CourseForm
    formset_class = TeacherCourseFormSet
    success_redirect = "course-list"


@require_http_methods(["POST"])
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    s = str(course)
    course.delete()
    messages.success(request, f"课程 {s} 删除成功！")
    return redirect("course-list")


def project_list(request):
    filter = ProjectFilter(request.GET or None, queryset=Project.objects.all())
    project_list = filter.qs.distinct()
    context = {"filter": filter, "project_list": project_list}

    return render(request, "teacher_app/project_list.html", context)


def paper_detail(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    context = {"paper": paper}
    return render(request, "teacher_app/paper_detail.html", context)


class ProjectCreateView(CreateWithInlinesView):
    model = Project
    form_class = ProjectForm
    formset_class = TeacherProjectFormSet
    success_redirect = "project-list"


class ProjectUpdateView(UpdateWithInlinesView):
    model = Project
    form_class = ProjectForm
    formset_class = TeacherProjectFormSet
    success_redirect = "project-list"


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {"project": project}
    return render(request, "teacher_app/project_detail.html", context)


@require_http_methods(["POST"])
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    s = str(project)
    project.delete()
    messages.success(request, f"项目 {s} 删除成功！")
    return redirect("project-list")


def paper_list(request):
    filter = PaperFilter(request.GET or None, queryset=Paper.objects.all())
    paper_list = filter.qs.distinct()
    context = {"filter": filter, "paper_list": paper_list}
    return render(request, "teacher_app/paper_list.html", context)


class PaperCreateView(CreateWithInlinesView):
    model = Paper
    form_class = PaperForm
    formset_class = TeacherPaperFormSet
    success_redirect = "paper-list"


class PaperUpdateView(UpdateWithInlinesView):
    model = Paper
    form_class = PaperForm
    formset_class = TeacherPaperFormSet
    success_redirect = "paper-list"


@require_http_methods(["POST"])
def paper_delete(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    s = str(paper)
    paper.delete()
    messages.success(request, f"论文 {s} 删除成功！")
    return redirect("paper-list")
