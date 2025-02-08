from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, User
from django.db import models


class Base(models.Model):
    GradeNum = (

        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    )

    base_grade = models.CharField(max_length=50, null=True, blank=True, choices=GradeNum)

    def __str__(self):
        return self.base_grade


class Classes(models.Model):
    base = models.ForeignKey(Base, null=True, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True, max_length=255, editable=True)

    def __str__(self):
        return f'{self.class_name}{self.base}'


class Course(models.Model):
    subject = models.CharField(max_length=500, null=True, blank=True)
    classes = models.ManyToManyField(Classes)
    grade_type = models.CharField(max_length=500, null=True, blank=True, editable=True)
    vahed = models.PositiveIntegerField(null=True, blank=True, max_length=1)

    def __str__(self):
        return self.subject


class UserAccountManager(BaseUserManager):
    def create_user(self, user_name, nationality, password=None):
        if not user_name:
            raise ValueError('')
        else:
            user = self.model(user_name=user_name, nationality=nationality)
            nationality = password
            user.set_password(nationality)
            user.save()
            return user

    def create_superuser(self, user_name, nationality, password):
        user = self.create_user(user_name=user_name, nationality=nationality, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class BaseFields(AbstractBaseUser):
    first_name = models.CharField(max_length=35, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=55, null=True, blank=True, verbose_name='خوانوادگی')
    user_name = models.PositiveIntegerField(null=False, blank=False, unique=True, verbose_name='نام کاربری')
    nationality = models.PositiveBigIntegerField(null=False, blank=False, verbose_name='کد ملی')
    home_number = models.PositiveIntegerField(null=True, blank=True, verbose_name='تلفن خانه')
    phone_number = models.PositiveIntegerField(null=True, blank=True, verbose_name='شماره تلفن')
    profile_photo = models.ImageField(upload_to='avatars/', default='avatar.png', null=True, blank=True)
    is_staff = models.BooleanField(default=False, verbose_name='مدیر')

    objects = UserAccountManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        return True

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['nationality']


class StudentAccount(BaseFields):
    father_name = models.CharField(max_length=35, null=True, blank=True, verbose_name='نام پدر')
    father_number = models.PositiveIntegerField(null=True, blank=True, verbose_name='شماره پدر')
    mother_number = models.PositiveIntegerField(null=True, blank=True, verbose_name='شماره مادر')
    status = models.BooleanField(null=True, verbose_name='وضعیت')
    classes = models.ForeignKey(Classes, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True, max_length=255, editable=True)
    graduate = models.BooleanField(default=False, verbose_name="test")
    allowed_to_promoted = models.BooleanField(default=True)
    objects = UserAccountManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} {self.classes}'
        else:
            return str(self.user_name)


class Staff(BaseFields):
    classes = models.ForeignKey(Classes, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True, allow_unicode=True, unique=True, max_length=255, editable=True)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    objects = UserAccountManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} {self.classes}'
        else:
            return str(self.user_name)


class TeacherAccount(BaseFields):
    classes = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE, verbose_name='نام درس')
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    objects = UserAccountManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return str(self.user_name)
