from django import forms

from Contact_Module.model import Contact, Notifications


class ContactForm(forms.Form):
    first_name = forms.CharField(label='نام', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg thick', 'placeholder': 'لطفا نام خود را وارد کنید', 'readonly': True, 'style': 'text-align: right;'}),
                                 error_messages={'required': 'پر کردن این فیلد اجباریست.', })
    last_name = forms.CharField(label='نام خوانوادگی', widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg thick', 'placeholder': 'لطفا نام خوانوادگی خود را وارد کنید', 'readonly': True, 'style': 'text-align: right;'}),
                                error_messages={'required': 'پر کردن این فیلد اجباریست.', })
    message = forms.CharField(label='متن پیام', widget=forms.Textarea(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'متن پیام را بنویسید', 'style': 'text-align: right;'}),
                              error_messages={'required': 'پر کردن این فیلد اجباریست.', })


class ReplyContactForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': '', }))


class NotificationForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': "پیام خود را بنویسید...",
    }))
