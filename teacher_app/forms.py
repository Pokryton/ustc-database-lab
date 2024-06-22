from django.forms import ModelForm
from crispy_forms.helper import FormHelper

from .models import Teacher

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ["id", "name", "gender", "title"]
        labels = {
            "id":  "工号",
            "name": "姓名",
            "gender": "性别",
            "title": "职称",
        }
