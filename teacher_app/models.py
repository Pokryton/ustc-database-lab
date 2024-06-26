from django.db import models
from django.db.models import Q

Gender = models.IntegerChoices("Gender", "男 女")

Title = models.IntegerChoices(
    "Title",
    "博士后 助教 讲师 副教授 特任教授 教授 助理研究员 特任副研究员 副研究员 特任研究员 研究员",
)

CourseKind = models.IntegerChoices("CourseKind", "本科生课程 研究生课程")

ProjectKind = models.IntegerChoices(
    "ProjectKind", "国家级项目 省部级项目 市厅级项目 企业合作项目 其它类型项目"
)

PAPER_KIND_CHOICES = [
    (1, "full paper"),
    (2, "short paper"),
    (3, "poster paper"),
    (4, "demo paper"),
]

PAPER_LEVEL_CHOICES = [
    (1, "CCF-A"),
    (2, "CCF-B"),
    (3, "CCF-C"),
    (4, "中文 CCF-A"),
    (5, "中文 CCF-B"),
    (6, "无级别"),
]


class Teacher(models.Model):
    id = models.CharField(max_length=5, primary_key=True, verbose_name="工号")
    name = models.CharField(max_length=200, verbose_name="姓名")
    gender = models.IntegerField(choices=Gender.choices, verbose_name="性别")
    title = models.IntegerField(choices=Title.choices, verbose_name="职称")

    class Meta:
        verbose_name = "教师"

    def __str__(self):
        return f"{self.id} {self.name}"


class Course(models.Model):
    id = models.CharField(max_length=256, primary_key=True, verbose_name="课程号")
    name = models.CharField(max_length=256, verbose_name="课程名")
    total_hours = models.PositiveIntegerField(verbose_name="总学时")
    kind = models.IntegerField(choices=CourseKind.choices, verbose_name="课程性质")
    teachers = models.ManyToManyField(Teacher, through="TeacherCourse")

    def __str__(self):
        return f"{self.id} {self.name}"


class Project(models.Model):
    id = models.CharField(max_length=256, primary_key=True, verbose_name="项目号")
    name = models.CharField(max_length=256, verbose_name="项目名称")
    source = models.CharField(max_length=256, verbose_name="项目来源")
    kind = models.IntegerField(choices=ProjectKind.choices, verbose_name="项目类型")
    total_fund = models.FloatField(verbose_name="总经费")
    start_year = models.PositiveIntegerField(verbose_name="开始年份")
    end_year = models.PositiveIntegerField(verbose_name="结束年份")
    teachers = models.ManyToManyField(Teacher, through="TeacherProject")

    def __str__(self):
        return f"{self.id} {self.name}"


class Paper(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name="序号")
    title = models.CharField(max_length=256, verbose_name="论文名称")
    pub_source = models.CharField(max_length=256, verbose_name="发表源")
    pub_year = models.DateField(verbose_name="发表年份")
    kind = models.IntegerField(choices=PAPER_KIND_CHOICES, verbose_name="类型")
    level = models.IntegerField(choices=PAPER_LEVEL_CHOICES, verbose_name="级别")
    teachers = models.ManyToManyField(Teacher, through="TeacherPaper")

    def __str__(self):
        return f"{self.id} {self.title}"


class TeacherCourse(models.Model):
    SEMESTER_CHOICES = {
        1: "春季学期",
        2: "夏季学期",
        3: "秋季学期",
    }

    teacher = models.ForeignKey("Teacher", on_delete=models.PROTECT)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    year = models.PositiveIntegerField(verbose_name="年份")
    semester = models.IntegerField(choices=SEMESTER_CHOICES, verbose_name="学期")
    hours = models.PositiveIntegerField(verbose_name="学时")

    def __str__(self):
        return f"{self.teacher.id} {self.course.id}"


class TeacherProject(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.PROTECT)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(verbose_name="排名")
    fund = models.FloatField(verbose_name="承担经费")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "project"],
                name="unique_teacher_project",
            ),
            models.UniqueConstraint(
                fields=["project", "rank"],
                name="unique_project_rank",
            )
        ]

    def __str__(self):
        return f"{self.teacher.id} {self.project.id}"


class TeacherPaper(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.PROTECT)
    paper = models.ForeignKey("Paper", on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(verbose_name="排名")
    corresp = models.BooleanField(verbose_name="是否通讯作者")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "paper"],
                name="unique_teacher_paper",
            ),
            models.UniqueConstraint(
                fields=["paper", "rank"],
                name="unique_paper_rank",
            ),
            models.UniqueConstraint(
                fields=["paper"],
                condition=Q(corresp=True),
                name="unique_paper_corresp",
            )
        ]

    def __str__(self):
        return f"{self.teacher.id} {self.paper.id}"
