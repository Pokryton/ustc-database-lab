from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db import transaction

from .models import *
from .forms import *
from .filters import *


def index(request):
    return redirect(reverse_lazy("teacher"))


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

    context = {"form": form, "formset": formset}
    return render(request, "teacher_app/course_form.html", context)


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

    context = {"form": form, "formset": formset}
    return render(request, "teacher_app/course_form.html", context)


def course_delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.POST:
        course.delete()
        return redirect(reverse_lazy("course"))

    context = {"object": course}
    return render(request, "teacher_app/course_confirm_delete.html", context)
