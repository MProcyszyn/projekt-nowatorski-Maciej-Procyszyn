from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee, CompetenceMatrix, EmployeeCompetence


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=Employee)
def assign_competences_to_new_employee(sender, instance, created, **kwargs):
    print("test dwa")

    if created:
        competences = CompetenceMatrix.objects.filter(employee_group=instance.employee_group)
        for competence in competences:
            if not EmployeeCompetence.objects.filter(employee=instance, matrix_entry=competence).exists():
                EmployeeCompetence.objects.create(
                    employee=instance,
                    matrix_entry=competence,
                    skill_level=None
                )


@receiver(post_save, sender=Employee)
def update_employee_competences(sender, instance, **kwargs):
    current_group = instance.employee_group
    if current_group:
        valid_competences = CompetenceMatrix.objects.filter(employee_group=current_group)
        valid_competence_ids = valid_competences.values_list('id', flat=True)

        EmployeeCompetence.objects.filter(
            employee=instance
        ).exclude(matrix_entry_id__in=valid_competence_ids).delete()

        existing_competence_ids = EmployeeCompetence.objects.filter(
            employee=instance
        ).values_list('matrix_entry_id', flat=True)

        missing_competences = valid_competences.exclude(id__in=existing_competence_ids)

        for competence in missing_competences:
            EmployeeCompetence.objects.create(
                employee=instance,
                matrix_entry=competence,
                skill_level=None
            )
