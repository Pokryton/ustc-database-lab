from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Teacher
from .forms import TeacherForm

def index(request):
    context = {}
    return render(request, "teacher_app/index.html", context)


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
