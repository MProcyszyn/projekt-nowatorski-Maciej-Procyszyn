# Generated by Django 4.2.11 on 2024-11-21 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onboarding_API', '0009_employee_hire_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('validity_period', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('is_done', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to='onboarding_API.employee')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='onboarding_API.training')),
            ],
        ),
    ]
