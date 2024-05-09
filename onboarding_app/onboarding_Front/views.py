from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from onboarding_API.models import Employee

# Create your views here.


@login_required()
def main_page(response):
    return render(response, "base.html", {})


def logout_page(response):
    return render(response, "logout.html", {})


def about_page(response):
    return render(response, "about.html", {})


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
    record = Employee.objects.get(pk=1)
    return render(response, "your_team.html", {'record': record})


def work_time_page(response):
    return render(response, "work_time.html", {})