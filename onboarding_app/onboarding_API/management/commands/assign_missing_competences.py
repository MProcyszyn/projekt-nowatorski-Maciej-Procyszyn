from django.core.management.base import BaseCommand
from onboarding_API.models import Employee, EmployeeCompetence, CompetenceMatrix

class Command(BaseCommand):
    help = "Assign missing competences to employees based on their group"

    def handle(self, *args, **kwargs):
        assigned_count = 0

        # Pobierz wszystkie kompetencje
        competences = CompetenceMatrix.objects.all()

        for competence in competences:
            # Pobierz pracowników z odpowiedniej grupy
            employees_in_group = Employee.objects.filter(employee_group=competence.employee_group)

            for employee in employees_in_group:
                # Sprawdź, czy kompetencja jest już przypisana
                if not EmployeeCompetence.objects.filter(employee=employee, matrix_entry=competence).exists():
                    # Przypisz kompetencję, jeśli jej brakuje
                    EmployeeCompetence.objects.create(
                        employee=employee,
                        matrix_entry=competence,
                        skill_level=None  # Domyślna wartość dla poziomu umiejętności
                    )
                    assigned_count += 1

        self.stdout.write(f"Successfully assigned {assigned_count} missing competences.")
