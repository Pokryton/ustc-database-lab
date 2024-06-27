from django.db import models
from django.db.models import F, Q


class Teacher(models.Model):
    GENDER_CHOICES = {
        1: "男",
        2: "女",
    }

    TITLE_CHOICES = {
        1: "博士后",
        2: "助教",
        3: "讲师",
        4: "副教授",
        5: "特任教授",
        6: "教授",
        7: "助理研究员",
        8: "特任副研究员",
        9: "副研究员",
        10: "特任研究员",
        11: "研究员",
    }

    id = models.CharField(max_length=5, primary_key=True, verbose_name="工号")
    name = models.CharField(max_length=200, verbose_name="姓名")
    gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name="性别")
    title = models.IntegerField(choices=TITLE_CHOICES, verbose_name="职称")

    class Meta:
        verbose_name = "教师"

    def __str__(self):
        return f"{self.id} {self.name}"


class Course(models.Model):
    COURSE_KIND_CHOICES = {
        1: "本科生课程",
        2: "研究生课程",
    }

    id = models.CharField(max_length=256, primary_key=True, verbose_name="课程号")
    name = models.CharField(max_length=256, verbose_name="课程名")
    total_hours = models.PositiveIntegerField(verbose_name="总学时")
    kind = models.IntegerField(choices=COURSE_KIND_CHOICES, verbose_name="课程性质")
    teachers = models.ManyToManyField(Teacher, through="TeacherCourse")

    class Meta:
        verbose_name = "课程"

    def __str__(self):
        return f"{self.id} {self.name}"


class Project(models.Model):
    PROJECT_KIND_CHOICES = {
        1: "国家级项目",
        2: "省部级项目",
        3: "市厅级项目",
        4: "企业合作项目",
        5: "其它类型项目",
    }

    id = models.CharField(max_length=256, primary_key=True, verbose_name="项目号")
    name = models.CharField(max_length=256, verbose_name="项目名称")
    source = models.CharField(max_length=256, verbose_name="项目来源")
    kind = models.IntegerField(choices=PROJECT_KIND_CHOICES, verbose_name="项目类型")
    total_fund = models.FloatField(verbose_name="总经费")
    start_year = models.PositiveIntegerField(verbose_name="开始年份")
    end_year = models.PositiveIntegerField(verbose_name="结束年份")
    teachers = models.ManyToManyField(Teacher, through="TeacherProject")

    class Meta:
        verbose_name = "项目"
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_year__lte=F("end_year")),
                name="start_year_lte_end_year",
                violation_error_message="开始年份应小于或等于结束年份",
            )
        ]

    def __str__(self):
        return f"{self.id} {self.name}"


class Paper(models.Model):
    PAPER_KIND_CHOICES = {
        1: "full paper",
        2: "short paper",
        3: "poster paper",
        4: "demo paper",
    }

    PAPER_LEVEL_CHOICES = {
        1: "CCF-A",
        2: "CCF-B",
        3: "CCF-C",
        4: "中文 CCF-A",
        5: "中文 CCF-B",
        6: "无级别",
    }

    id = models.PositiveIntegerField(primary_key=True, verbose_name="序号")
    title = models.CharField(max_length=256, verbose_name="论文名称")
    source = models.CharField(max_length=256, verbose_name="发表源")
    pub_year = models.DateField(verbose_name="发表年份")
    kind = models.IntegerField(choices=PAPER_KIND_CHOICES, verbose_name="类型")
    level = models.IntegerField(choices=PAPER_LEVEL_CHOICES, verbose_name="级别")
    teachers = models.ManyToManyField(Teacher, through="TeacherPaper")

    class Meta:
        verbose_name = "论文"

    def __str__(self):
        return f"{self.id} {self.title}"


class TeacherCourse(models.Model):
    SEMESTER_CHOICES = {
        1: "春季学期",
        2: "夏季学期",
        3: "秋季学期",
    }

    teacher = models.ForeignKey(
        "Teacher", on_delete=models.PROTECT, verbose_name="教师"
    )
    course = models.ForeignKey("Course", on_delete=models.CASCADE, verbose_name="课程")
    year = models.PositiveIntegerField(verbose_name="年份")
    semester = models.IntegerField(choices=SEMESTER_CHOICES, verbose_name="学期")
    hours = models.PositiveIntegerField(verbose_name="学时")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "course", "year", "semester"],
                name="unique_teacher_course_year_semester",
                violation_error_message="授课教师重复",
            ),
        ]

    def __str__(self):
        return f"{self.teacher.id} {self.course.id}"


class TeacherProject(models.Model):
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.PROTECT, verbose_name="教师"
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, verbose_name="项目"
    )
    rank = models.PositiveIntegerField(verbose_name="排名")
    fund = models.FloatField(verbose_name="承担经费")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "project"],
                name="unique_teacher_project",
                violation_error_message="承担教师重复",
            ),
            models.UniqueConstraint(
                fields=["project", "rank"],
                name="unique_project_rank",
                violation_error_message="排名重复",
            ),
        ]

    def __str__(self):
        return f"{self.teacher.id} {self.project.id}"


class TeacherPaper(models.Model):
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.PROTECT, verbose_name="教师"
    )
    paper = models.ForeignKey("Paper", on_delete=models.CASCADE, verbose_name="论文")
    rank = models.PositiveIntegerField(verbose_name="排名")
    corresp = models.BooleanField(verbose_name="是否通讯作者")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "paper"],
                name="unique_teacher_paper",
                violation_error_message="作者重复",
            ),
            models.UniqueConstraint(
                fields=["paper", "rank"],
                name="unique_paper_rank",
                violation_error_message="排名重复",
            ),
            models.UniqueConstraint(
                fields=["paper"],
                condition=Q(corresp=True),
                name="unique_paper_corresp",
                violation_error_message="一篇论文只能有一个通讯作者",
            ),
        ]

    def __str__(self):
        return f"{self.teacher.id} {self.paper.id}"
