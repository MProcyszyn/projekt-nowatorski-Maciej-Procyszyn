from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import RegisterForm, EmployeeForm
from onboarding_API.models import Employee, EmployeeGroup
from django.contrib import messages

# Create your views here.


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
                        employee_group=EmployeeGroup.objects.get(group_id=1)
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


@login_required()
def about_page(request):
    employee = Employee.objects.get(user=request.user)
    user_groups = request.user.groups.values_list('name', flat=True)
    context = {
        'employee': employee,
        'user_groups': user_groups,
    }
    return render(request, "about.html", context)


@login_required()
def your_team_page(request):
    employee = Employee.objects.get(user=request.user)
    employee.user.username = employee.user.username.capitalize()
    user_groups = request.user.groups.values_list('name', flat=True)
    context = {
        'employee': employee,
        'user_groups': user_groups,
    }

    return render(request, "your_team.html", context)


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
            user = user_form.save()

            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            return redirect('/')
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
