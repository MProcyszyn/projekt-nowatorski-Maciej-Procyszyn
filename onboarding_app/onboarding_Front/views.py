from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm
from django.forms import DateInput
from .forms import RegisterForm, EmployeeForm, TrainingForm, EmployeeTrainingForm, CustomLoginForm, EmployeeProficiencyLevelForm, CompetenceMatrixForm
from onboarding_API.models import Employee, EmployeeGroup, EmployeeCompetence, EmployeeTraining, CompetenceMatrix, Training
from itertools import groupby
from operator import attrgetter


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm


def logout_page(request):
    messages.success(request, "You have been logged out successfully.")
    return render(request, "logout.html", {})


def register_page(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()

                    employee = Employee(
                        user=user,
                        experience="",
                        phone_nr="",
                        employee_group=EmployeeGroup.objects.get(id=1)
                    )

                    employee.save()

                return redirect("/")
            except Exception as error:
                form.add_error(None, f"Something went wrong. {error}")
    else:
        form = RegisterForm()

    return render(request, "registration/registration.html", {'form': form})


@login_required()
def main_page(request):
    employee = Employee.objects.get(user=request.user)
    user_groups = request.user.groups.values_list('name', flat=True)
    context = {
        'employee': employee,
        'user_groups': user_groups,
    }
    return render(request, "base.html",  context)


@login_required
def about_page(request):
    employee = Employee.objects.get(user=request.user)
    trainings = employee.trainings.all()
    competences = employee.competences.all()

    context = {
        'employee': employee,
        'trainings': trainings,
        'competences': competences,
    }
    return render(request, "about.html", context)


@login_required
def your_team_page(request):
    employee = Employee.objects.get(user=request.user)
    user = request.user
    employees = Employee.objects.filter(created_by=user)

    highlight_employee_id = request.session.pop('highlight_employee_id', None)

    context = {
        'employee': employee,
        'employees': employees,
        'user': user,
        'highlight_employee_id': highlight_employee_id,
    }

    return render(request, "your_team.html", context)


@login_required
def edit_employee_page(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    user = employee.user

    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=user)
        employee_form = EmployeeForm(request.POST, instance=employee)

        user_form.fields.pop('password', None)
        user_form.fields = {
            'username': user_form.fields['username'],
            'email': user_form.fields['email'],
        }

        if user_form.is_valid() and employee_form.is_valid():
            user_form.save()
            updated_employee = employee_form.save()
            updated_employee.save()

            messages.success(request, "Employee details updated successfully!")
            return redirect('employee_detail', employee_id=employee.id)
    else:
        user_form = UserChangeForm(instance=user)
        user_form.fields['username'].widget.attrs['class'] = 'form-control'
        user_form.fields['email'].widget.attrs['class'] = 'form-control'

        employee_form = EmployeeForm(instance=employee)

        user_form.fields.pop('password', None)
        user_form.fields = {
            'username': user_form.fields['username'],
            'email': user_form.fields['email'],
        }

        employee_form.fields['hire_date'].widget = DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select hire date',
            }
        )

    context = {
        'employee': employee,
        'user_form': user_form,
        'employee_form': employee_form,
    }
    return render(request, 'edit_employee.html', context)


@login_required
def delete_employee_page(request, employee_id):
    employee_to_delete = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        try:
            employee_to_delete.user.delete()
            messages.success(request, f"Employee {employee_to_delete.user.username} has been successfully deleted.")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
        return redirect('your_team')


@login_required
def employee_detail_page(request, employee_id):
    employee = Employee.objects.get(user=request.user)
    employee_obj = get_object_or_404(Employee, id=employee_id)
    trainings = EmployeeTraining.objects.filter(employee=employee_obj)
    competences = EmployeeCompetence.objects.filter(employee=employee_obj).order_by('matrix_entry__id')

    context = {
        'employee': employee,
        'employee_obj': employee_obj,
        'trainings': trainings,
        'competences': competences,
    }

    return render(request, 'employee_detail.html', context)


@login_required()
def add_employee_page(request):
    employee = Employee.objects.get(user=request.user)
    user_groups = request.user.groups.values_list('name', flat=True)

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        employee_form = EmployeeForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()

                    new_employee = employee_form.save(commit=False)
                    new_employee.user = user
                    new_employee.created_by = request.user
                    new_employee.save()

                    request.session['highlight_employee_id'] = new_employee.id
                    request.session.modified = True

                    competences = CompetenceMatrix.objects.filter(employee_group=new_employee.employee_group)
                    for competence in competences:
                        EmployeeCompetence.objects.create(
                            employee=new_employee,
                            matrix_entry=competence,
                            skill_level=None
                        )

                return redirect('your_team')
            except Exception as error:
                user_form.add_error(None, f"Something went wrong: {error}")
        else:
            print("User Form Errors:", user_form.errors)
            print("Employee Form Errors:", employee_form.errors)

    else:
        user_form = RegisterForm()
        employee_form = EmployeeForm()

    context = {
        'employee': employee,
        'user_groups': user_groups,
        'user_form': user_form,
        'employee_form': employee_form,
    }
    return render(request, 'add_employee.html', context)


@login_required()
def add_training_page(request):
    employee = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Training type has been successfully created.")
            return redirect('/')
    else:
        form = TrainingForm()

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'add_training.html', context)


@login_required()
def assign_training_page(request):
    employee = Employee.objects.get(user=request.user)
    employee_name = request.GET.get('employee_name', None)
    employee_obj = None

    if employee_name:
        employee_obj = Employee.objects.filter(user__username=employee_name).first()

    if request.method == 'POST':
        form = EmployeeTrainingForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Training has been successfully assigned.")
                return redirect('employee_detail', employee_id=form.cleaned_data['employee'].id)
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        if employee_obj:
            form = EmployeeTrainingForm(initial={'employee': employee_obj})
        else:
            form = EmployeeTrainingForm()

    context = {
        'employee': employee,
        'form': form,
        'employee_obj': employee_obj,
    }
    return render(request, 'assign_training.html', context)


@login_required
def all_trainings_page(request):
    employee = Employee.objects.get(user=request.user)
    trainings = Training.objects.all().order_by('id')

    context = {
        'employee': employee,
        'trainings': trainings,
    }
    return render(request, 'all_trainings.html', context)


@login_required
def edit_training_page(request, training_id):
    employee = Employee.objects.get(user=request.user)
    training = get_object_or_404(EmployeeTraining, id=training_id)

    if request.method == 'POST':
        form = EmployeeTrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, "Training updated successfully!")
            return redirect('employee_detail', employee_id=training.employee.id)
    else:
        form = EmployeeTrainingForm(instance=training)

    context = {
        'employee': employee,
        'form': form,
        'training': training,
    }
    return render(request, 'edit_training.html', context)


@login_required
def delete_training(request, training_id):
    training = get_object_or_404(Training, id=training_id)
    if request.method == 'POST':
        training.delete()
        messages.success(request, "Training deleted successfully.")
        return redirect('all_trainings')

    context = {
        'training': training,
    }


@login_required
def edit_employee_training(request, training_id):
    employee = Employee.objects.get(user=request.user)
    employee_training = get_object_or_404(EmployeeTraining, id=training_id)

    if request.method == 'POST':
        form = EmployeeTrainingForm(request.POST, instance=employee_training)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Training updated successfully!")
                return redirect('employee_detail', employee_id=employee_training.employee.id)
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = EmployeeTrainingForm(instance=employee_training)

    context = {
        'employee': employee,
        'employee_training': employee_training,
        'form': form,
    }
    return render(request, 'edit_employee_training.html', context)


@login_required
def all_competences_page(request):
    employee = Employee.objects.get(user=request.user)
    competences = CompetenceMatrix.objects.all().order_by('employee_group')
    grouped_competences = {
        group: list(items)
        for group, items in groupby(competences, key=attrgetter('employee_group'))
    }

    highlight_competence_id = request.session.pop('highlight_competence_id', None)

    context = {
        'employee': employee,
        'grouped_competences': grouped_competences,
        'highlight_competence_id': highlight_competence_id,

    }
    return render(request, 'all_competences.html', context)


@login_required
def edit_competence_page(request, competence_id):
    competence = get_object_or_404(CompetenceMatrix, id=competence_id)
    employee = Employee.objects.get(user=request.user)

    if request.method == 'POST':
        form = CompetenceMatrixForm(request.POST, instance=competence)
        if form.is_valid():
            form.save()
            messages.success(request, "Competence updated successfully!")
            return redirect('all_competences')
    else:
        form = CompetenceMatrixForm(instance=competence)

    context = {
        'employee': employee,

        'form': form,
        'competence': competence,
    }
    return render(request, 'edit_competence.html', context)


@login_required
def delete_competence(request, competence_id):
    competence = get_object_or_404(CompetenceMatrix, id=competence_id)
    if request.method == 'POST':
        competence.delete()
        messages.success(request, "Competence deleted successfully.")
        return redirect('all_competences')

    context = {
        'competence': competence,
    }


@login_required
def create_competence_view(request):
    employee = Employee.objects.get(user=request.user)
    if request.method == 'POST':
        form = CompetenceMatrixForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    competence = form.save()

                    employees_in_group = Employee.objects.filter(employee_group=competence.employee_group)

                    for emp in employees_in_group:
                        EmployeeCompetence.objects.create(
                            employee=emp,
                            matrix_entry=competence,
                            skill_level=None
                        )

                    request.session['highlight_competence_id'] = competence.id
                    request.session.modified = True

                    messages.success(request, "Competence has been successfully created and assigned.")
                    return redirect('all_competences')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
    else:
        form = CompetenceMatrixForm()

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'create_competence.html', context)


@login_required
def edit_employee_proficiency_level(request, competence_id):
    employee = Employee.objects.get(user=request.user)
    competence = get_object_or_404(EmployeeCompetence, id=competence_id)
    if request.method == 'POST':
        form = EmployeeProficiencyLevelForm(request.POST, instance=competence)
        if form.is_valid():
            form.save()
            messages.success(request, "Competence level updated successfully!")
            return redirect('employee_detail', employee_id=competence.employee.id)
    else:
        form = EmployeeProficiencyLevelForm(instance=competence)

    context = {
        'employee': employee,
        'form': form,
        'competence': competence,
    }
    return render(request, 'edit_employee_proficiency_level.html', context)


@login_required
def delete_employee_training(request, training_id):
    training_assignment = get_object_or_404(EmployeeTraining, id=training_id)
    employee_id = training_assignment.employee.id

    training_assignment.delete()
    messages.success(request, "Training assignment successfully deleted.")

    return redirect('employee_detail', employee_id=employee_id)
