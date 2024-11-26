from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, EmployeeForm, TrainingForm, EmployeeTrainingForm, CustomLoginForm, EmployeeCompetenceForm
from onboarding_API.models import Employee, EmployeeGroup, EmployeeCompetence, EmployeeTraining


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
    # Pobierz aktualnie zalogowanego pracownika
    employee = Employee.objects.get(user=request.user)

    # Pobierz szkolenia przypisane do pracownika
    trainings = employee.trainings.all()

    # Pobierz kompetencje przypisane do pracownika
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
    # Pobierz aktualnie zalogowanego użytkownika
    user = request.user

    # Pobierz pracowników zatrudnionych przez aktualnego użytkownika
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
def work_time_page(request):
    employee = Employee.objects.get(user=request.user)
    user_groups = request.user.groups.values_list('name', flat=True)
    context = {
        'employee': employee,
        'user_groups': user_groups,
    }
    return render(request, "work_time.html", context)


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

                return redirect('/')
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
    if request.method == 'POST':
        form = EmployeeTrainingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Training has been successfully assigned.")
            return redirect('/')
    else:
        form = EmployeeTrainingForm()

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'assign_training.html', context)


@login_required
def employee_competences_page(request, employee_id):
    employee = Employee.objects.get(user=request.user)
    employee_obj = get_object_or_404(Employee, id=employee_id)
    competences = EmployeeCompetence.objects.filter(employee=employee_obj)
    context = {
        'employee': employee,
        'employee_obj': employee_obj,
        'competences': competences,
    }
    return render(request, 'employee_competences.html', context)


@login_required
def edit_competence_page(request, competence_id):
    employee = Employee.objects.get(user=request.user)
    competence = get_object_or_404(EmployeeCompetence, id=competence_id)

    if request.method == 'POST':
        form = EmployeeCompetenceForm(request.POST, instance=competence)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('employee_competences', args=[competence.employee.id]))
    else:
        form = EmployeeCompetenceForm(instance=competence)

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
