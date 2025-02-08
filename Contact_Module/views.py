from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from Contact_Module.model import Contact
from Contact_Module.forms import ContactForm
from Authentication_Module.models import StudentAccount


# Create your views here.


class ContactView(View):
    def get(self, request):
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        else:
            initial_data = {
                'first_name': '',
                # 'last_name': '',
            }
        form = ContactForm(initial=initial_data)

        return render(request, 'Contact_Module/contact_us.html', {
            'form': form,
        })

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            message = form.cleaned_data.get('message')
            student: StudentAccount = StudentAccount.objects.filter(first_name=first_name, last_name=last_name).first()
            x = Contact(first_name=first_name, last_name=last_name, message=message, student_id=student.id)
            x.save()
            return redirect(reverse('contact_us_page'))

        return render(request, 'Contact_Module/contact_us.html', {
            'form': form,
        })
