from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from onboarding_API.models import Employee, EmployeeGroup, Training, EmployeeTraining, EmployeeCompetence
from crispy_forms.helper import FormHelper


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
        label='Employee group',
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    experience = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your experience'})
    )
    phone_nr = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Employee
        fields = ('employee_group', 'experience', 'phone_nr')


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

    class Meta:
        model = EmployeeTraining
        fields = ['employee', 'training', 'completion_date', 'is_done']


class EmployeeCompetenceForm(forms.ModelForm):
    class Meta:
        model = EmployeeCompetence
        fields = ['skill_level']
        widgets = {
            'skill_level': forms.Select(attrs={'class': 'form-control'}),
        }