from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee, CompetenceMatrix, EmployeeCompetence
from django.utils.timezone import now


@receiver(post_save, sender=User)
def manage_employee_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Employee.objects.create(
                user=instance,
                employee_group=EmployeeGroup.objects.first(),
                hire_date=now().date(),
            )
        except Exception:
            pass
    else:
        if hasattr(instance, 'employee'):
            try:
                instance.employee.save()
            except Exception:
                pass


@receiver(post_save, sender=Employee)
def manage_employee_competences(sender, instance, created, **kwargs):
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

        for competence in valid_competences:
            if competence.id not in existing_competence_ids:
                EmployeeCompetence.objects.create(
                    employee=instance,
                    matrix_entry=competence,
                    skill_level=None
                )


@receiver(post_save, sender=EmployeeCompetence)
def prevent_duplicate_competences(sender, instance, **kwargs):
    if EmployeeCompetence.objects.filter(
        employee=instance.employee,
        matrix_entry=instance.matrix_entry
    ).count() > 1:
        instance.delete()