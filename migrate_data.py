import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from main.models import ExerciseType, ExerciseLog, Pushup, Achievement
from django.contrib.auth.models import User

def run_migration():
    print("Inicjalizacja typów ćwiczeń...")
    pompki, created = ExerciseType.objects.get_or_create(name="Pompki", unit="powtórzenia")
    ExerciseType.objects.get_or_create(name="Przysiady", unit="powtórzenia")
    ExerciseType.objects.get_or_create(name="Podciągnięcia", unit="powtórzenia")

    print("Migracja danych z Pushup do ExerciseLog...")
    pushups = Pushup.objects.all()
    count = 0
    for p in pushups:
        # Sprawdzamy czy już nie istnieje, żeby nie dublować przy ponownym uruchomieniu
        if not ExerciseLog.objects.filter(user=p.user, date=p.date, exercise_type=pompki).exists():
            ExerciseLog.objects.create(
                user=p.user,
                exercise_type=pompki,
                date=p.date,
                value=p.pushups
            )
            count += 1
    print(f"Zmigrowano {count} rekordów.")

    print("Inicjalizacja osiągnięć...")
    achievements = [
        ("Pierwszy krok", "Dodaj swój pierwszy trening", "star", "total_reps", 1),
        ("Tysięcznik", "Wykonaj łącznie 1000 powtórzeń", "trophy", "total_reps", 1000),
        ("Wytrwały", "Utrzymaj streak przez 7 dni", "fire", "streak", 7),
        ("Mistrz regularności", "Utrzymaj streak przez 30 dni", "crown", "streak", 30),
    ]

    for name, desc, icon, req_type, req_val in achievements:
        Achievement.objects.get_or_create(
            name=name,
            description=desc,
            badge_icon=icon,
            requirement_type=req_type,
            requirement_value=req_val
        )
    print("Osiągnięcia zainicjalizowane.")

if __name__ == "__main__":
    run_migration()
