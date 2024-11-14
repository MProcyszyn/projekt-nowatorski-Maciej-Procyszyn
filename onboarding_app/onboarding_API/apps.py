from django.apps import AppConfig
from django.db.models.signals import post_migrate


class OnboardingApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'onboarding_API'

    def ready(self):
        post_migrate.connect(self.create_groups)

    def create_groups(self, **kwargs):
        from .models import EmployeeGroup
        groups = [('Rookie', 1), ('IT', 2), ('HR', 3), ('Team Leader', 4)]
        for group in groups:
            EmployeeGroup.objects.get_or_create(name=group[0], group_id=group[1])

