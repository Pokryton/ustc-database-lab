from django.shortcuts import render


def index(req):
    ctx = {}
    return render(req, "teacher_app/index.html", ctx)
