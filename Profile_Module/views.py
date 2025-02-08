from itertools import groupby
import jalali_date
from django.contrib.auth import logout
from django.db.models import Max, Min, Count, Q
from django.db.models.functions import TruncDate, TruncTime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import reverse
from django.views.generic import View
from Contact_Module.forms import *
from Contact_Module.model import ContactReply
from Main_Module.signals import *
from Main_Module.model import *
from Profile_Module.forms import *

# Create your views here.


class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm()

        return render(request, 'Profile_Module/change_password.html', {
            'form': form,
        })

    def post(self, request):

        form = ChangePasswordForm(request.POST)
        if form.is_valid():

            current_user = StudentAccount.objects.filter(id=request.user.id).first()
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')

            if current_user:

                if current_user.check_password(current_password):

                    current_user.set_password(new_password)
                    current_user.save()
                    logout(request)

                    return redirect(reverse('student_login_page'))

                else:
                    if current_user.password == current_password:

                        current_user.set_password(new_password)
                        current_user.save()
                        logout(request)

                        return redirect(reverse('student_login_page'))

                    else:
                        form.add_error('current_password', 'رمز عبور فعلی نادرست است.')
            else:
                current_user = Staff.objects.filter(id=request.user.id).first()

                if current_user:

                    if current_user.check_password(current_password):

                        current_user.set_password(new_password)
                        current_user.save()
                        logout(request)

                        return redirect(reverse('staff_login_page'))
                    else:
                        if current_user.password == current_password:
                            current_user.set_password(new_password)
                            current_user.save()
                            logout(request)

                            return redirect(reverse('staff_login_page'))
                        else:
                            form.add_error('current_password', 'رمز عبور فعلی نادرست است.')
                else:
                    current_user = Staff.objects.filter(id=request.user.id).first()
                    if current_user:
                        if current_user.check_password(current_password):
                            current_user.set_password(new_password)
                            current_user.save()
                            logout(request)

                            return redirect(reverse('staff_login_page'))

                        else:
                            if current_user.password == current_password:
                                current_user.set_password(new_password)
                                current_user.save()
                                logout(request)

                                return redirect(reverse('staff_login_page'))

                            else:
                                form.add_error('current_password', 'رمز عبور فعلی نادرست است.')

        return render(request, 'Profile_Module/change_password.html', {'form': form, })


def change_pfp(request):
    user = BaseFields.objects.filter(id=request.user.id).first()
    form = UploadProfile(instance=user)

    if request.method == 'POST':
        form = UploadProfile(request.POST, request.FILES, instance=user)

        if form is not None:
            form.save()
            return redirect('/profile')

    context = {'user': user, 'form': form}
    return render(request, 'Profile_Module/pfp.html', context)


def profile_view(request):

    abslout_date = jalali_date.date2jalali(datetime.date.today()).strftime('%Y-%m-%d')
    date = jalali_date.date2jalali(datetime.date.today())
    month_filter = date.month

    print(month_filter)

    profile = ClCourses.objects.filter(student=request.user.id).count()
    detail = BaseFields.objects.filter(id=request.user.id).first()
    teacher = ClCourses.objects.filter(student=request.user.id).select_related('subject').order_by('slug')
    classes = Classes.objects.all()

    group = Group.objects.get(name='staff')
    principal = Group.objects.get(name='principal')
    teach = Group.objects.get(name='teacher')
    messages_count = ContactReply.objects.filter(contact__first_name=request.user.first_name,
                                                 contact__last_name=request.user.last_name,
                                                 read_by_student=False).count()

    grouped_assignments = {}

    for key, group in groupby(teacher, key=lambda x: x.slug):
        grouped_assignments[key] = [teacher.slug for teacher in group]

    # months = str(month)
    month_count = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    jalali_months = ['دی', 'بهمن', 'فروردین', 'اسفند', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان',
                     'آذر', 'دی']

    # current_month = jalali_months[int(month)]

    context = {
        'profile': profile, 'detail': detail, 'group': group,
        'messages_count': messages_count, 'classes': classes,
        'teacher': teacher, 'grouped_assignments': grouped_assignments,
        'principal': principal, 'teach': teach, 'current_month':month_filter
    }

    return render(request, 'Profile_Module/profile.html', context)


def edit_personal_info(request):
    user = BaseFields.objects.filter(id=request.user.id).first()
    form = EditInfoForm(instance=user)

    if request.method == 'POST':

        form = EditInfoForm(request.POST, instance=user)
        if form.is_valid:
            form.save()

            return redirect('/profile')

    context = {'user': user, 'form': form}
    return render(request, 'Profile_Module/edit_info.html', context)


def inbox_user(request):
    reply = ContactReply.objects.filter(contact__first_name=request.user.first_name,
                                        contact__last_name=request.user.last_name)
    reply.filter(read_by_student=False).update(read_by_student=True)
    send_messages = Contact.objects.filter(first_name=request.user.first_name, last_name=request.user.last_name)
    user = Staff.objects.filter(role__name='principal').first()

    messages = sorted(
        list(reply) + list(send_messages),
        key=lambda x: x.created_at
    )

    context = {
        'messages': messages,
        'user': user,
    }

    return render(request, 'Profile_Module/inbox.html', context)


@check_role_staff
@check_role_principal
def all_contacts(request):
    contacts = (
        Contact.objects.values('first_name', 'last_name', 'student__profile_photo').annotate(
            date=Max(TruncDate('date')), time=Min(TruncTime('time')),
            unread=Count('read_by_admin', filter=Q(read_by_admin=False)))
        .order_by('-time'))

    context = {
        'contacts': contacts,
    }

    return render(request, 'Profile_Module/contacts.html', context)


@check_role_staff
@check_role_principal
def reply_contact(request, first_name, last_name):
    user = get_object_or_404(StudentAccount, first_name=first_name, last_name=last_name)
    contacts = Contact.objects.filter(first_name=user.first_name, last_name=user.last_name)
    contacts.filter(read_by_admin=False).update(read_by_admin=True)
    replies = ContactReply.objects.filter(contact__first_name=user.first_name,
                                          contact__last_name=user.last_name)

    messages = sorted(
        list(replies) + list(contacts), key=lambda x: x.created_at
    )

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        reply_message = request.POST.get('message')
        if reply_message:
            contact_instance = contacts.last()
            new_reply = ContactReply.objects.create(contact=contact_instance, message=reply_message)
            new_reply.save()

            return JsonResponse({
                "status": "success",
                "message": reply_message,
            })
        return JsonResponse({"status": "error", "message": "متن پیام خالی است."})

    context = {
        'messages': messages,
        'user': user,
    }
    return render(request, 'Profile_Module/reply_contact.html', context)


@check_role_staff
@check_role_principal
def send_notification(request, role):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = NotificationForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            new_notification = Notifications(role=role, message=message)
            new_notification.save()

            return JsonResponse({
                'status': 'success',
                'message': message,
                'date': new_notification.created_at.strftime('%Y/%m/%d'),
                'time': new_notification.created_at.strftime('%H:%M:%S')
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'فرم معتبر نیست.'}, status=400)

    all_notification = Notifications.objects.filter(role=role)
    form = NotificationForm()
    context = {
        'form': form, 'all_notification': all_notification, 'role': role,
    }
    return render(request, 'Profile_Module/send_notifications.html', context)


@check_role_staff
@check_role_principal
def show_contacts(request):
    x = {
        'student': {
            'last_notification': Notifications.objects.filter(role='student').last(),
        },
        'teacher': {
            'last_notification': Notifications.objects.filter(role='teacher').last(),
        },
        'staff': {
            'last_notification': Notifications.objects.filter(role='staff').last(),
        },
    }

    for role, details in x.items():
        notification = details['last_notification']
        if notification:
            details['message'] = notification.message
            details['date'] = jalali_date.date2jalali(notification.date).strftime('%Y/%m/%d')
            details['time'] = notification.time.strftime('%H:%M')
        else:
            details['message'] = None
            details['date'] = None
            details['time'] = None

    context = {
        'x': x,
    }

    return render(request, 'Profile_Module/show_contacts.html', context)


def show_notifications(request):
    principal = Group.objects.get(name='principal')
    user = request.user
    if hasattr(user, 'staff') and user.staff:
        if user.staff.role == Group.objects.get(name='teacher'):
            notification = Notifications.objects.filter(role='teacher').order_by('created_at')
        elif user.staff.role == Group.objects.get(name='staff'):
            notification = Notifications.objects.filter(role='staff').order_by('created_at')
        else:
            notification = Notifications.objects.filter(role='student').order_by('created_at')
    else:
        notification = Notifications.objects.filter(role='student').order_by('created_at')

    context = {
        'notification': notification, 'principal': principal,
    }

    return render(request, 'Profile_Module/show_notifications.html', context)
