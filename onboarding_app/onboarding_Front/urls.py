from django.contrib import admin
from django.urls import path, include
from . import views
from .views import CustomLoginView


urlpatterns = [
    path('', views.main_page, name='Front'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', views.logout_page, name='logout'),
    path('about', views.about_page, name='about'),
    path("", include("django.contrib.auth.urls")),
    path("registration", views.register_page, name="registration"),
    path('your_team', views.your_team_page, name='your_team'),
    path('add_employee', views.add_employee_page, name='add_employee'),
    path('session_security/', include('session_security.urls')),
    path('assign_training', views.assign_training_page, name='assign_training'),
    path('add_training', views.add_training_page, name='add_training'),
    path('all_competences/', views.all_competences_page, name='all_competences'),
    path('competence/<int:competence_id>/edit/', views.edit_competence_page, name='edit_competence'),
    path('employee/<int:employee_id>/', views.employee_detail_page, name='employee_detail'),
    path('training/<int:training_id>/edit/', views.edit_training_page, name='edit_training'),
    path('create_competence/', views.create_competence_view, name='create_competence'),

]
