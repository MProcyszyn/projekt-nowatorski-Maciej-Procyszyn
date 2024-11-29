from django.apps import AppConfig
from django.db.models.signals import post_migrate


class OnboardingApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'onboarding_API'

    def ready(self):
        import onboarding_API.signals

    def create_default_groups(sender, **kwargs):
        groups = ['Rookie', 'IT', 'HR', 'Team Leader', 'Maintenance']
        for group in groups:
            EmployeeGroup.objects.get_or_create(name=group)

    post_migrate.connect(create_default_groups)
