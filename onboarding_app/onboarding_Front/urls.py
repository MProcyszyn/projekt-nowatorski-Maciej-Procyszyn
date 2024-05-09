from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='Front'),
    path('logout', views.logout_page, name='logout'),
    path('about', views.about_page, name='about'),
    path("", include("django.contrib.auth.urls")),
    path("registration", views.register_page, name="registration"),
    path('your_team', views.your_team_page, name='your_team'),
    path('work_time', views.work_time_page, name='work_time'),
]
