from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db import transaction

from .models import *
from .forms import *
from .filters import *


def index(request):
    return redirect(reverse_lazy("teacher-list"))


def teacher_search(request):
    if request.method == "POST":
        id = request.POST.get("id")
        # TODO
        teacher_list = Teacher.objects.filter(id__icontains=id)
    else:
        teacher_list = Teacher.objects.order_by("id")

    context = {"teacher_list": teacher_list}
    return render(request, "teacher_app/teacher_list.html", context)


def teacher_add(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f"教师 {teacher.name} 登记成功！")
            return redirect("teacher")
    else:
        form = TeacherForm()

    return render(request, "teacher_app/teacher_add.html", {"form": form})


def teacher_detail(request, pk):
    teacher_info = Teacher.objects.filter(pk=pk).first()
    teacher_course = TeacherCourse.objects.filter(teacher__id=pk).first()
    return render(request, "teacher_app/teacher_detail.html", {"form": form})


def course_list(request):
    filter = CourseFilter(request.GET or None, queryset=Course.objects.all())
    course_list = filter.qs.distinct()
    context = {"filter": filter, "course_list": course_list}

    return render(request, "teacher_app/course_list.html", context)


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {"course": course}
    return render(request, "teacher_app/course_detail.html", context)


def course_add(request):
    form = CourseForm(request.POST or None)
    formset = TeacherCourseFormSet(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            course = form.save(commit=False)
            formset.instance = course

            if formset.is_valid():
                course.save()
                formset.save()
                messages.success(request, f"课程 {course.name} 登记成功！")
                return redirect(reverse_lazy("course-list"))

    context = {
        "model": "course",
        "model_name": "课程",
        "form": form,
        "formset": formset,
    }
    return render(request, "teacher_app/form.html", context)


def course_update(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    form = CourseForm(request.POST or None, instance=course)
    form.fields["id"].disabled = True
    formset = TeacherCourseFormSet(request.POST or None, instance=course)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            course = form.save()
            formset.instance = course
            formset.save()
            messages.success(request, f"课程 {course.name} 更新成功！")
            return redirect(reverse_lazy("course-list"))

    context = {
        "model": "course",
        "model_name": "课程",
        "form": form,
        "formset": formset,
    }
    return render(request, "teacher_app/form.html", context)


def course_delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.POST:
        course.delete()
        return redirect(reverse_lazy("course-list"))

    context = {"object": course}
    return render(request, "teacher_app/confirm_delete.html", context)


def project_list(request):
    filter = ProjectFilter(request.GET or None, queryset=Project.objects.all())
    project_list = filter.qs.distinct()
    context = {"filter": filter, "project_list": project_list}

    return render(request, "teacher_app/project_list.html", context)


def project_add(request):
    form = ProjectForm(request.POST or None)
    formset = TeacherProjectFormSet(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            project = form.save(commit=False)
            formset.instance = project

            if formset.is_valid():
                project.save()
                formset.save()
                messages.success(request, f"项目 {project.name} 登记成功！")
                return redirect(reverse_lazy("project-list"))

    context = {
        "model": "project",
        "model_name": "项目",
        "form": form,
        "formset": formset,
    }
    return render(request, "teacher_app/form.html", context)


def project_update(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    form = ProjectForm(request.POST or None, instance=project)
    form.fields["id"].disabled = True
    formset = TeacherProjectFormSet(request.POST or None, instance=project)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            project = form.save()
            formset.instance = project
            formset.save()
            messages.success(request, f"项目 {project.name} 更新成功！")
            return redirect(reverse_lazy("project-list"))

    context = {
        "model": "project",
        "model_name": "项目",
        "form": form,
        "formset": formset,
    }
    return render(request, "teacher_app/form.html", context)


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {"project": project}
    return render(request, "teacher_app/project_detail.html", context)


def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.POST:
        project.delete()
        return redirect(reverse_lazy("project-list"))

    context = {"object": project}
    return render(request, "teacher_app/confirm_delete.html", context)


def paper_list(request):
    filter = PaperFilter(request.GET or None, queryset=Paper.objects.all())
    paper_list = filter.qs.distinct()
    context = {"filter": filter, "paper_list": paper_list}

    return render(request, "teacher_app/paper_list.html", context)

