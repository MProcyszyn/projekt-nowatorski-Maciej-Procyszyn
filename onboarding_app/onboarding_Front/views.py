from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from .forms import RegisterForm, EmployeeForm, TrainingForm, EmployeeTrainingForm, CustomLoginForm, EmployeeCompetenceLevelForm, CompetenceMatrixForm
from onboarding_API.models import Employee, EmployeeGroup, EmployeeCompetence, EmployeeTraining, CompetenceMatrix
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

    context = {
        'employee': employee,
        'employees': employees,
        'user': user,
    }

    return render(request, "your_team.html", context)


@login_required
def employee_detail_page(request, employee_id):
    employee = Employee.objects.get(user=request.user)
    employee_obj = get_object_or_404(Employee, id=employee_id)
    trainings = EmployeeTraining.objects.filter(employee=employee_obj)
    competences = EmployeeCompetence.objects.filter(employee=employee_obj)

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

                    employee = employee_form.save(commit=False)
                    employee.user = user
                    employee.created_by = request.user
                    employee.save()

                return redirect('your_team')
            except Exception as error:
                user_form.add_error(None, f"Something went wrong: {error}")
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
                return redirect('your_team')
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
def all_competences_page(request):
    employee = Employee.objects.get(user=request.user)
    competences = CompetenceMatrix.objects.all().order_by('employee_group')
    grouped_competences = {
        group: list(items)
        for group, items in groupby(competences, key=attrgetter('employee_group'))
    }

    context = {
        'employee': employee,
        'grouped_competences': grouped_competences,
    }
    return render(request, 'all_competences.html', context)


@login_required
def edit_competence_page(request, competence_id):
    employee = Employee.objects.get(user=request.user)
    competence = get_object_or_404(EmployeeCompetence, id=competence_id)
    if request.method == 'POST':
        form = EmployeeCompetenceLevelForm(request.POST, instance=competence)
        if form.is_valid():
            form.save()
            messages.success(request, "Competence updated successfully!")
            return redirect('employee_detail', employee_id=competence.employee.id)
    else:
        form = EmployeeCompetenceLevelForm(instance=competence)

    context = {
        'employee': employee,
        'form': form,
        'competence': competence,
    }
    return render(request, 'edit_competence.html', context)


@login_required
def edit_training_page(request, training_id):
    employee = Employee.objects.get(user=request.user)
    training = get_object_or_404(EmployeeTraining, id=training_id)

    if request.method == 'POST':
        form = EmployeeTrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
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
