from django import forms


class LoginForm(forms.Form):
    user_name = forms.IntegerField(
        label='نام کاربری',
        error_messages={
            'required': 'پر کردن این فیلد اجباریست.',
        },
        widget=forms.NumberInput(
            attrs={
                'class': '',
                'id': 'username',
                'placeholder': ' ',
            }
        )
    )
    password = forms.CharField(
        label='رمز عبور',
        error_messages={
            'required': 'پر کردن این فیلد اجباریست.',
        },
        widget=forms.PasswordInput(
            attrs={
                'class': '',
                'id': 'password',
                'placeholder': ' ',
            }
        )
    )


class AddStudentForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    nationality = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    home_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    father_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    father_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    mother_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )


class AddStaffForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    nationality = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    home_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    father_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    father_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    mother_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )


class AddPersonnelForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    nationality = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    home_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )


class AddTeacherForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': '',
            }
        )
    )
    nationality = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    home_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )
    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': '',
            }
        )
    )


class ForgotPasswordForm(forms.Form):
    user_name = forms.IntegerField(
        label='نام کاربری',
        error_messages={
            'required': 'پر کردن این فیلد اجباریست.',
        },
        widget=forms.NumberInput(
            attrs={
                'class': '',
                'id': 'username',
                'placeholder': ' ',
            }
        )
    )
