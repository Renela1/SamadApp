from django.db import models
from Authentication_Module.models import StudentAccount


# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=25, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=40, null=True, blank=True, verbose_name='نام خوانوادگی')
    message = models.TextField(max_length=350, null=False, blank=False, verbose_name='متن پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در')
    date = models.DateField(auto_now_add=True, null=True, verbose_name='تاریخ')
    time = models.TimeField(auto_now_add=True, null=True, verbose_name='ساعت')
    read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط مدیر')
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='دانش آموز')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ContactReply(models.Model):
    student = models.ForeignKey(StudentAccount, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='دانش آموز')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, verbose_name='پیام')
    message = models.CharField(max_length=200, null=True, blank=True, verbose_name='جواب پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ساخته شده در')
    date = models.DateField(auto_now_add=True, null=True, verbose_name='تاریخ')
    time = models.TimeField(auto_now_add=True, null=True, verbose_name='ساعت')
    read_by_student = models.BooleanField(default=False, verbose_name='خوانده شده توسط دانش آموز')


class Notifications(models.Model):
    role = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=120, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False, verbose_name='')
    date = models.DateField(auto_now_add=True, null=True, blank=True, editable=False, verbose_name='')
    time = models.TimeField(auto_now_add=True, null=True, blank=True, editable=False, verbose_name='')
