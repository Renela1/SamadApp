from django.contrib import admin
from .model import *
from django.contrib.auth.admin import UserAdmin
from Authentication_Module.models import *
from Contact_Module.model import *
from Profile_Module.models import *


# Register your models here.


class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code")


admin.site.register(Grades)
admin.site.register(FinalGrades)
admin.site.register(Course)
admin.site.register(Date)
admin.site.register(Attendance)
admin.site.register(ClCourses)
admin.site.register(Description)
