from django import forms
from django.core.exceptions import ValidationError
from Authentication_Module.models import Staff, BaseFields, StudentAccount


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'current-password',
            }
        )
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'new-password',
            }
        )
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'confirm-password',
            }
        )
    )

    def clean_confirm_new_password(self):
        password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_new_password')
        if password == confirm_password:
            return password
        else:
            raise ValidationError('رمز عبور جدید و تکرار آن با هم مغایرت دارند.')


class EditInfoForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["first_name", "last_name", "user_name", "phone_number"]


class UploadProfile(forms.ModelForm):
    class Meta:
        model = BaseFields
        fields = ['profile_photo']
