from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateInput
from onboarding_API.models import Employee, EmployeeGroup, Training, EmployeeTraining, EmployeeCompetence, CompetenceMatrix, ProficiencyLevel
from crispy_forms.helper import FormHelper
from django.utils.timezone import now
import re


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class EmployeeForm(forms.ModelForm):
    employee_group = forms.ModelChoiceField(
        queryset=EmployeeGroup.objects.all(),
        initial=lambda: EmployeeGroup.objects.filter(name='Rookie').first(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    experience = forms.ModelChoiceField(
        queryset=ProficiencyLevel.objects.all(),
        initial=lambda: ProficiencyLevel.objects.filter(proficiency_level='Shadow').first(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    phone_nr = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )

    hire_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select hire date',
            }
        ),
        initial=now().date  # Use the current date as the default value
    )

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        self.fields['employee_group'].choices = [
            (group.id, group.name) for group in EmployeeGroup.objects.all()
        ]

        self.fields['experience'].choices = [
            (level.id, level.proficiency_level) for level in ProficiencyLevel.objects.all()
        ]

        self.fields['hire_date'].widget = DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select hire date',
                'value': now().date()

            }
        )

    def clean_phone_nr(self):
        phone_nr = self.cleaned_data.get('phone_nr')
        if not re.match(r'^\+?\d{9,15}$', phone_nr):
            raise ValidationError('Enter a valid phone number (e.g., +123456789).')
        return phone_nr

    class Meta:
        model = Employee
        fields = ('employee_group', 'experience', 'phone_nr', 'hire_date')


class TrainingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter training name'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter training description'
        })
        self.fields['validity_period'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Select validity period'
        })

    class Meta:
        model = Training
        fields = ['name', 'description', 'validity_period']


class EmployeeTrainingForm(forms.ModelForm):
    class Meta:
        model = EmployeeTraining
        fields = ['employee', 'training', 'completion_date', 'is_done']

    completion_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Select completion date'
        }),
        label="Completion Date"
    )

    def __init__(self, *args, **kwargs):
        super(EmployeeTrainingForm, self).__init__(*args, **kwargs)

        self.fields['employee'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['training'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['is_done'].widget.attrs.update({
            'class': 'form-check-input',
        })

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        training = cleaned_data.get('training')

        if EmployeeTraining.objects.filter(
            employee=employee, training=training
                ).exclude(id=self.instance.id).exists():
            raise ValidationError("This training has already been assigned to this employee.")

        return cleaned_data


class EmployeeProficiencyLevelForm(forms.ModelForm):
    class Meta:
        model = EmployeeCompetence
        fields = ['skill_level']
        widgets = {
            'skill_level': forms.Select(attrs={'class': 'form-control'}),
        }


class CompetenceMatrixForm(forms.ModelForm):
    class Meta:
        model = CompetenceMatrix
        fields = ['employee_group', 'skill_description']
        widgets = {
            'employee_group': forms.Select(attrs={'class': 'form-control'}),
            'skill_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
