from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from Authentication_Module.forms import *
from Authentication_Module.models import *

print('hello')

# Create your views here.

class StudentsLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))

        form = LoginForm()

        return render(request, 'Authentication_Module/student_login.html', {
            'form': form,
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            user_pass = form.cleaned_data.get('password')
            user: StudentAccount = StudentAccount.objects.filter(user_name=user_name).first()
            if user:
                correct_password = user.check_password(user_pass)
                if correct_password:
                    login(request, user)
                    return redirect(reverse('profile'))
                else:
                    if user.password == user_pass:
                        login(request, user)
                        return redirect(reverse('profile'))
                    else:
                        form.add_error('password', 'رمز عبور نادرست است.')
            else:
                form.add_error('user_name', 'دانش آموزی با اطلاعات وارد شده وجود ندارد!')

        return render(request, 'Authentication_Module/student_login.html', {
            'form': form,
        })


class StaffLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))

        form = LoginForm()

        return render(request, 'Authentication_Module/staff_login.html', {
            'form': form,
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            user_pass = form.cleaned_data.get('password')
            user: Staff = Staff.objects.filter(user_name=user_name).first()
            if user:
                correct_password = user.check_password(user_pass)
                if correct_password:
                    login(request, user)
                    return redirect(reverse('profile'))
                else:
                    if user.password == user_pass:
                        login(request, user)
                        return redirect(reverse('profile'))
                    else:
                        form.add_error('password', 'رمز عبور نادرست است.')
            else:
                form.add_error('user_name', 'کاربری با اطلاعات وارد شده وجود ندارد!')

        return render(request, 'Authentication_Module/staff_login.html', {
            'form': form,
        })


class AddStudentView(View):
    def get(self, request):
        form = AddStudentForm()

        return render(request, 'Authentication_Module/add_student.html', {
            'form': form,
        })

    def post(self, request):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user_name = form.cleaned_data.get('user_name')
            nationality = form.cleaned_data.get('nationality')
            home_number = form.cleaned_data.get('home_number')
            phone_number = form.cleaned_data.get('phone_number')
            father_name = form.cleaned_data.get('father_name')
            father_number = form.cleaned_data.get('father_number')
            mother_number = form.cleaned_data.get('mother_number')
            user: StudentAccount = StudentAccount.objects.filter(user_name=user_name, nationality=nationality).first()
            if user:
                form.add_error('user_name', 'نام کاربری یا کد ملی تکراری میباشد.')
            else:
                new_user = StudentAccount(
                    first_name=first_name, last_name=last_name, user_name=user_name, nationality=nationality,
                    home_number=home_number, phone_number=phone_number, father_name=father_name,
                    father_number=father_number, mother_number=mother_number
                )
                new_user.set_password(str(nationality))
                new_user.save()
                return redirect(reverse('add_student_page'))

        return render(request, 'Authentication_Module/add_student.html', {
            'form': form,
        })


class AddStaffView(View):
    def get(self, request):
        form = AddStaffForm()

        return render(request, 'Authentication_Module/add_staff.html', {
            'form': form,
        })

    def post(self, request):
        form = AddStaffForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user_name = form.cleaned_data.get('user_name')
            nationality = form.cleaned_data.get('nationality')
            home_number = form.cleaned_data.get('home_number')
            phone_number = form.cleaned_data.get('phone_number')
            father_name = form.cleaned_data.get('father_name')
            father_number = form.cleaned_data.get('father_number')
            mother_number = form.cleaned_data.get('mother_number')
            user: Staff = Staff.objects.filter(user_name=user_name, nationality=nationality).first()
            if user:
                form.add_error('user_name', 'نام کاربری یا کد ملی تکراری میباشد.')
            else:
                new_user = Staff(
                    first_name=first_name, last_name=last_name, user_name=user_name, nationality=nationality,
                    home_number=home_number, phone_number=phone_number, father_name=father_name,
                    father_number=father_number, mother_number=mother_number
                )
                new_user.set_password(str(nationality))
                new_user.save()
                return redirect(reverse('add_student_page'))

        return render(request, 'Authentication_Module/add_student.html', {
            'form': form,
        })


class LogoutView(View):
    def get(self, request):
        if request.user.is_staff is True:
            logout(request)
            return redirect(reverse('staff_login_page'))
        else:
            logout(request)
            return redirect(reverse('student_login_page'))


class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()

        return render(request, 'Authentication_Module/forgot_password.html', {
            'form': form,
        })

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            user: StudentAccount = StudentAccount.objects.filter(user_name=user_name).first()
            if user:
                user.set_password(str(user.nationality))
                user.save()
                return redirect(reverse('student_login_page'))
            else:
                user: TeacherAccount = TeacherAccount.objects.filter(user_name=user_name).first()
                if user:
                    user.set_password(str(user.nationality))
                    user.save()
                    return redirect(reverse('staff_login_page'))
                else:
                    user: Staff = Staff.objects.filter(user_name=user_name).first()
                    if user:
                        user.set_password(str(user.nationality))
                        user.save()
                        return redirect(reverse('staff_login_page'))
                    else:
                        form.add_error('user_name', 'کاربری با مشخصات وارد شده وجود ندارد.')

        return render(request, 'Authentication_Module/forgot_password.html', {
            'form': form,
        })
