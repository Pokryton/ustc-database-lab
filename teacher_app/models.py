from django.db import models

Gender = models.IntegerChoices("Gender", "男 女")

Title = models.IntegerChoices(
    "Title",
    "博士后 助教 讲师 副教授 特任教授 教授 助理研究员 特任副研究员 副研究员 特任研究员 研究员",
)

CourseKind = models.IntegerChoices("CourseKind", "本科生课程 研究生课程")

ProjectKind = models.IntegerChoices(
    "ProjectKind", "国家级项目 省部级项目 市厅级项目 企业合作项目 其它类型项目"
)

Semester = models.IntegerChoices("Semester", "春季学期 夏季学期 秋季学期")

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
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=200)
    gender = models.IntegerField(choices=Gender.choices)
    title = models.IntegerField(choices=Title.choices)

    def __str__(self):
        return f"{self.id} {self.name}"


class Course(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=256)
    hours = models.IntegerField()
    kind = models.IntegerField(choices=CourseKind.choices)
    teachers = models.ManyToManyField(Teacher, through="TeacherCourse")

    def __str__(self):
        return f"{self.id} {self.name}"


class Project(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=256)
    source = models.CharField(max_length=256)
    kind = models.IntegerField(choices=ProjectKind.choices)
    total_fund = models.FloatField()
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    teachers = models.ManyToManyField(Teacher, through="TeacherProject")

    def __str__(self):
        return f"{self.id} {self.name}"


class Paper(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    pub_sourse = models.CharField(max_length=256)
    pub_year = models.DateField()
    kind = models.IntegerField(choices=PAPER_KIND_CHOICES)
    level = models.IntegerField(choices=PAPER_LEVEL_CHOICES)
    teachers = models.ManyToManyField(Teacher, through="TeacherPaper")

    def __str(self):
        return f"{self.id} {self.title}"


class TeacherCourse(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.PROTECT)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField(choices=Semester.choices)
    hour = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "course"],
                name="unique_teacher_course",
            )
        ]

    def __str__(self):
        return f"{self.teacher.id} {self.course.id}"


class TeacherProject(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.PROTECT)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    rank = models.IntegerField()
    fund = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "project"],
                name="unique_teacher_project",
            )
        ]

    def __str__(self):
        return f"{self.teacher.id} {self.project.id}"


class TeacherPaper(models.Model):
    teacher = models.ForeignKey("Teacher", on_delete=models.PROTECT)
    paper = models.ForeignKey("Paper", on_delete=models.CASCADE)
    rank = models.IntegerField()
    corresp = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "paper"],
                name="unique_teacher_paper",
            )
        ]

    def __str__(self):
        return f"{self.teacher.id} {self.paper.id}"
