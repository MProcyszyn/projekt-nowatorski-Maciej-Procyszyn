from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from onboarding_API.models import Employee
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class EmployeeForm(forms.ModelForm):
    EMPLOYEE_GROUP_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'Human Resources'),
        ('MT', 'Maintenance'),
    ]
    employee_group = forms.ChoiceField(choices=EMPLOYEE_GROUP_CHOICES, label='Employee group', required=True)
    experience = forms.CharField(required=True)
    phone_nr = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Employee
        fields = ('employee_group', 'experience', 'phone_nr')
