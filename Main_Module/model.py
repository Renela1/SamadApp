import datetime
import jdatetime
from django.db import models
from Authentication_Module.models import StudentAccount, Course, Staff, Classes
from django_jalali.db import models as jmodels


# -----------------------------------------#
# NOTE: STUDENT RELATED TABLES AND FIELDS #
# -----------------------------------------#


class Date(models.Model):
    month = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.month


class Grades(models.Model):
    Poudman = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date = jmodels.jDateField(null=True, blank=True, default=jdatetime.date.today())
    time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now())
    grades_100 = models.FloatField(max_length=20, null=True, blank=True, default=1.0)
    grades_20 = models.FloatField(max_length=20, null=True, blank=True, default=1.0)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, to_field='slug', related_name='slug2', null=True)
    attended = models.BooleanField(null=True, default=False)
    grade_type = models.CharField(max_length=500, null=True, blank=True, editable=True)
    passed = models.BooleanField(null=True, default=True)
    poudman = models.IntegerField(choices=Poudman, null=True, blank=True)
    archived = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f'{self.student} {self.subject}'


class ClCourses(models.Model):
    
    student = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    course_type = models.CharField(max_length=500, null=True, blank=True, editable=True)
    slug = models.ForeignKey(Classes, on_delete=models.CASCADE, to_field='slug', related_name='slug4', null=True)

    def __str__(self):
        return f'{self.student} {self.subject}'


class Attendance(models.Model):
    student = models.ForeignKey(StudentAccount, null=True, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False, verbose_name='زنگ اول')
    completed2 = models.BooleanField(default=False, verbose_name='زنگ دوم')
    completed3 = models.BooleanField(default=False, verbose_name='زنگ سوم')
    completed4 = models.BooleanField(default=False, verbose_name='زنگ چهارم')
    completion_date = models.DateField(null=True, blank=True)
    slug = models.ForeignKey(Classes, on_delete=models.CASCADE, to_field='slug', related_name='slugger', null=True)


class Description(models.Model):
    classes = models.ForeignKey(Classes, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    text_box = models.CharField(max_length=500, null=True, blank=True)


class FinalGrades(models.Model):
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date = jmodels.jDateField(null=True, blank=True, default=jdatetime.date.today())
    time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now())
    overal_grade = models.FloatField(max_length=20, null=True, blank=True, default=1.0)
    grades_amali = models.FloatField(max_length=20, null=True, blank=True, default=1.0)
    grades_theory = models.FloatField(max_length=20, null=True, blank=True, default=1.0)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, to_field='slug', related_name='slug5', null=True)
    turn = models.IntegerField(null=True, default=False, max_length=20)
    grade_type = models.CharField(max_length=500, null=True, blank=True, editable=True)
    passed = models.BooleanField(null=True, default=True)
    vahed = models.PositiveIntegerField(null=True, blank=True, max_length=1)

    def __str__(self):
        return f'{self.student} {self.subject}'

# -----------------------------------------#
# ----------END OF STUDENT MODELS----------#
# -----------------------------------------#
