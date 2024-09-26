from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from onboarding_API.models import Employee

# Create your views here.


@login_required()
def main_page(response):
    user_groups = response.user.groups.values_list('name', flat=True)
    context = {
        'user_groups': user_groups,
    }
    return render(response, "base.html", context)


def logout_page(response):
    return render(response, "logout.html", {})


def about_page(response):
    user_groups = response.user.groups.values_list('name', flat=True)
    context = {
        'user_groups': user_groups,
    }
    return render(response, "about.html", context)


def register_page(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = RegisterForm()
    return render(response, "registration/registration.html", {'form': form})


def your_team_page(response):
    user_groups = response.user.groups.values_list('name', flat=True)
    record = Employee.objects.get(pk=1)
    context = {
        'user_groups': user_groups,
        'record': record,
    }

    return render(response, "your_team.html", context)


def work_time_page(response):
    user_groups = response.user.groups.values_list('name', flat=True)
    context = {
        'user_groups': user_groups,
    }
    return render(response, "work_time.html", context)


def add_employee_page(response):
    user_groups = response.user.groups.values_list('name', flat=True)
    context = {
        'user_groups': user_groups,
    }

    return render(response, "add_employee.html", context)
