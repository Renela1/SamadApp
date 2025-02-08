from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .model import *
from Authentication_Module.models import StudentAccount


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter email-username", "class": "form-control"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={"placeholder": "Enter password", "class": "form-control"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={"placeholder": "Confirm password", "class": "form-control"}))

    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]


class ReportCardForm(ModelForm):
    class Meta:
        model = Grades
        fields = '__all__'
        exclude = ["slug", "sum", "description", "author"]
        labels = {
            'student': 'نام دانش آموز', 'subject': 'عنوان درس', 'date': 'تاریخ', 'grades': 'نمره هفته اول',
            'grades2': 'نمره هفته دوم',
            'grades3': 'نمره هفته سوم', 'grades4': 'نمره هفته چهارم', 'classes': 'کلاس',
        }
        widgets = {
            'student': forms.Select(attrs={}), 'subject': forms.Select(attrs={}),
            'grades': forms.NumberInput(attrs={'class': '', }), 'grades2': forms.NumberInput(attrs={'class': '', }),
            'grades3': forms.NumberInput(attrs={'class': '', }), 'grades4': forms.NumberInput(attrs={'class': '', }),
            'classes': forms.Select(attrs={}), 'date': forms.Select(attrs={'class': '', }),
        }


class AddReportCardForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = '__all__'
        exclude = ["slug", "sum"]
        labels = {
            'student': '', 'subject': '', 'date': 'تاریخ', 'grades': 'نمره هفته اول', 'grades2': 'نمره هفته دوم',
            'grades3': 'نمره هفته سوم', 'grades4': 'نمره هفته چهارم', 'classes': '',
        }
        widgets = {
            'student': forms.Select(attrs={'hidden': True, }), 'subject': forms.Select(attrs={'hidden': True, }),
            'date': forms.Select(attrs={'class': '', }), 'grades': forms.NumberInput(attrs={'class': '', }),
            'grades2': forms.NumberInput(attrs={'class': '', }),
            'grades3': forms.NumberInput(attrs={'class': '', }),
            'grades4': forms.NumberInput(attrs={'class': '', }), 'classes': forms.Select(attrs={'hidden': True, })
        }


class TodoForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'completed', 'completed2', 'completed3', 'completed4', 'slug', 'id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['slug'].label = ''
        self.fields['student'].widget.attrs['class'] = 'readonly'


class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = '__all__'


class GradesForm(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['grades_100', 'grades_20', 'student', 'classes', 'subject',
                  'attended']  # List all the fields you need in the form

        widgets = {

            'date': forms.DateInput(attrs={'class': 'readonly', 'readonly': True}),
            'attended': forms.CheckboxInput(attrs={'class': ''})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make specific fields readonly
        self.fields['subject'].widget.attrs['class'] = 'readonly-select'
        self.fields['classes'].widget.attrs['class'] = 'readonly-select'
        self.fields['student'].widget.attrs['class'] = 'readonly-select'

        self.fields['student'].label = ''
        self.fields['subject'].label = ''
        self.fields['grades_100'].label = ''
        self.fields['grades_20'].label = ''

        self.fields['grades_100'].widget.attrs['class'] = 'field'
        self.fields['grades_20'].widget.attrs['class'] = 'field'

class GradesForm_B(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['grades_100', 'grades_20', 'student', 'classes', 'subject', 'poudman',
                  'attended']  # List all the fields you need in the form

        widgets = {

            'date': forms.DateInput(attrs={'class': 'readonly', 'readonly': True}),
            'attended': forms.CheckboxInput(attrs={'class': ''})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make specific fields readonly
        self.fields['subject'].widget.attrs['class'] = 'readonly-select'
        self.fields['classes'].widget.attrs['class'] = 'readonly-select'
        self.fields['student'].widget.attrs['class'] = 'readonly-select'

        self.fields['student'].label = ''
        self.fields['subject'].label = ''
        self.fields['grades_100'].label = ''
        self.fields['grades_20'].label = ''

        self.fields['grades_100'].widget.attrs['class'] = 'field'
        self.fields['grades_20'].widget.attrs['class'] = 'field'



class GradesForm_C(forms.ModelForm):
    class Meta:
        model = Grades
        fields = ['grades_20', 'student', 'classes', 'subject', 'attended']  # List all the fields you need in the form
        exclude = ['grades_100']
        widgets = {

            'date': forms.DateInput(attrs={'class': 'readonly', 'readonly': True}),
            'attended': forms.CheckboxInput(attrs={'class': ''})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make specific fields readonly
        self.fields['subject'].widget.attrs['class'] = 'readonly-select'
        self.fields['classes'].widget.attrs['class'] = 'readonly-select'
        self.fields['student'].widget.attrs['class'] = 'readonly-select'

        self.fields['student'].label = ''
        self.fields['subject'].label = ''
        self.fields['grades_20'].label = ''

        self.fields['grades_20'].widget.attrs['class'] = 'field'


class ClassOveral(forms.ModelForm):
    class Meta:
        model = FinalGrades
        fields = ['overal_grade', 'student', 'classes', 'subject',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make specific fields readonly
        self.fields['subject'].widget.attrs['class'] = 'readonly-select'
        self.fields['classes'].widget.attrs['class'] = 'readonly-select'
        self.fields['student'].widget.attrs['class'] = 'readonly-select'

        self.fields['student'].label = ''
        self.fields['subject'].label = ''


class FinalFormGrade(forms.ModelForm):
    class Meta:
        model = FinalGrades
        fields = ['grades_amali', 'grades_theory', 'student', 'classes', 'subject',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make specific fields readonly
        self.fields['subject'].widget.attrs['class'] = 'readonly-select'
        self.fields['classes'].widget.attrs['class'] = 'readonly-select'
        self.fields['student'].widget.attrs['class'] = 'readonly-select'

        self.fields['student'].label = ''
        self.fields['subject'].label = ''
        self.fields['grades_amali'].label = 'نمره عملی'
        self.fields['grades_theory'].label = 'نمره تئوری '
        self.fields['grades_amali'].widget.attrs['class'] = 'field'
        self.fields['grades_theory'].widget.attrs['class'] = 'field'


class FinalFormGrade_C(forms.ModelForm):
    class Meta:
        model = FinalGrades
        fields = ['grades_theory', 'student', 'classes', 'subject',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make specific fields readonly
        self.fields['subject'].widget.attrs['class'] = 'readonly-select'
        self.fields['classes'].widget.attrs['class'] = 'readonly-select'
        self.fields['student'].widget.attrs['class'] = 'readonly-select'

        self.fields['student'].label = ''
        self.fields['subject'].label = ''
        self.fields['grades_theory'].label = 'نمره تئوری '

class TextForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs['class'] = 'readonly-select'
        self.fields['subject'].label = ''
        self.fields['date'].widget.attrs['class'] = 'readonly'
        self.fields['date'].label = ''

class StudentPromotion(forms.ModelForm):
    class Meta:
        model = StudentAccount
        fields = ['allowed_to_promoted', 'first_name', 'last_name']