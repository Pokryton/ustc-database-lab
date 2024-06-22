from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.db import transaction

from .models import Teacher, Course
from .forms import TeacherForm, CourseForm, TeacherCourseFormSet

def index(request):
    return render(request, "teacher_app/index.html")


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
            messages.success(request, f"教师 {teacher} 登记成功！")
            return redirect("teacher")
    else:
        form = TeacherForm(label_suffix="")

    return render(request, "teacher_app/teacher_add.html", {"form": form})


class CourseListView(ListView):
    model = Course
    template_name = "teacher_app/course.html"
    context_object_name = "course_list"
    ordering = ["id"]


class CourseDetailView(DetailView):
    model = Course
    template_name = "teacher_app/course_detail.html"
    context_object_name = "course"


class CourseCreateView(CreateView):
    model = Course
    fields = ["id", "name", "hours", "kind"]
    success_url = "/course/"

    def get_context_data(self, **kwargs):
        data = super(CourseCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data["formset"] = TeacherCourseFormSet(self.request.POST)
        else:
            data["formset"] = TeacherCourseFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
        return super(CourseCreateView, self).form_valid(form)
