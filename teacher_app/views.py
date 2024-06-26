from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from django.db import transaction

from .models import *
from .forms import *


def index(request):
    return redirect(reverse_lazy("teacher"))


def teacher_search(request):
    if request.method == "POST":
        id = request.POST.get("id")
        # TODO
        teacher_list = Teacher.objects.filter(id__icontains=id)
    else:
        teacher_list = Teacher.objects.order_by("id")

    return render(request, "teacher_app/teacher.html", {"teacher_list": teacher_list})


def teacher_add(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f"教师 {teacher.name} 登记成功！")
            return redirect("teacher")
    else:
        form = TeacherForm(label_suffix="")

    return render(request, "teacher_app/teacher_add.html", {"form": form})


def teacher_detail(request, pk):
    teacher_info = Teacher.objects.filter(pk=pk).first()
    teacher_course = TeacherCourse.objects.filter(teacher__id=pk).first()
    return render(request, "teacher_app/teacher_detail.html", {"form": form})


class CourseListView(ListView):
    model = Course
    template_name = "teacher_app/course.html"
    context_object_name = "course_list"
    ordering = ["id"]


class CourseDetailView(DetailView):
    model = Course
    template_name = "teacher_app/course_detail.html"
    context_object_name = "course"


def course_create(request):
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
                return redirect(reverse_lazy("course"))

    return render(
        request, "teacher_app/course_form.html", {"form": form, "formset": formset}
    )


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
            return redirect(reverse_lazy("course"))
        messages.warning(
            request, f"课程 {course.name} 更新不成功！<br> {formset.errors}"
        )

    return render(
        request, "teacher_app/course_form.html", {"form": form, "formset": formset}
    )


# def course_delete(request, course_id):
class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy("course")
