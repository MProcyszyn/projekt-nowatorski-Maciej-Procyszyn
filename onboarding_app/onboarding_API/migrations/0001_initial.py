# Generated by Django 4.2.11 on 2024-05-09 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=100)),
                ('phone_nr', models.CharField(max_length=15)),
            ],
        ),
    ]
