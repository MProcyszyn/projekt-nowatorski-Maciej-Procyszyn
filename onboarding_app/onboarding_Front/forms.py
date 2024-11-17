from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from onboarding_API.models import Employee, EmployeeGroup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        group = forms.ModelChoiceField(queryset=EmployeeGroup.objects.all(), initial=EmployeeGroup.objects.get(name='Rookie'))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class EmployeeForm(forms.ModelForm):
    employee_group = forms.ModelChoiceField(queryset=EmployeeGroup.objects.all(), label='Employee group', required=True)
    experience = forms.CharField(required=True)
    phone_nr = forms.CharField(required=True)

    class Meta:
        model = Employee
        fields = ('employee_group', 'experience', 'phone_nr')

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        self.fields['employee_group'].choices = [
            (group.group_id, group.name) for group in EmployeeGroup.objects.all()
        ]
