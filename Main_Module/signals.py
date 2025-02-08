from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from .model import ClCourses, Course, Staff


def UnathenicatedUser(views_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:

            return redirect('login/')

        else:

            return views_func(request, *args, **kwargs)

    return wrapper_func


def AllowedUsers(allowed_roles=[]):
    def decorator(views_func):

        def wrapper_func(request, *args, **kwargs):

            group = None

            group = Group.objects.all()

            if group in allowed_roles:
                return views_func(request, *args, **kwargs)

            else:
                return HttpResponse('you are not authorized to view this page')

        return wrapper_func

    return decorator


def AdminOnly(views_func):
    def wrapper_function(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Other':
            return redirect('/')

        if group == 'Admin':
            return views_func(request, *args, **kwargs)

    return wrapper_function


def check_role_staff(views_func):
    def wrapper_function(request, *args, **kwargs):

        if request.user.staff.role == Group.objects.get(name='staff'):

            return views_func(request, *args, **kwargs)

        elif request.user.staff.role == Group.objects.get(name='principal'):

            return views_func(request, *args, **kwargs)

        else:
            return HttpResponse('شما به این صفحه دسترسی ندارید')

    return wrapper_function


def check_role_teacher(views_func):
    def wrapper_function(request, *args, **kwargs):

        if request.user.staff.role == Group.objects.get(name='teacher'):

            return views_func(request, *args, **kwargs)

        elif request.user.staff.role == Group.objects.get(name='principal'):

            return views_func(request, *args, **kwargs)

        else:
            return HttpResponse('شما به این صفحه دسترسی ندارید')

    return wrapper_function


def check_role_principal(views_func):
    def wrapper_function(request, *args, **kwargs):

        try:

            if request.user.staff.role == Group.objects.get(name='principal'):

                return views_func(request, *args, **kwargs)

            else:
                return HttpResponse('شما به این صفحه دسترسی ندارید')

        except:
            return HttpResponse('شما به این صفحه دسترسی ندارید')

    return wrapper_function
