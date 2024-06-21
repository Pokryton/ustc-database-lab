from django.contrib import admin

from .models import *

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Project)
admin.site.register(Paper)
admin.site.register(TeacherCourse)
admin.site.register(TeacherProject)
admin.site.register(TeacherPaper)
