from django.apps import AppConfig


class OnboardingFrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'onboarding_Front'


class OnboardingAppConfig(AppConfig):
    name = 'onboarding_Front'

    def ready(self):
        import onboarding_app.signals
