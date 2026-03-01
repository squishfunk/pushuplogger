from django import forms
from .models import ExerciseLog, ExerciseType

class Addnewlog(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ("exercise_type", "value")
        labels = {
            'exercise_type': 'Rodzaj ćwiczenia',
            'value': 'Liczba powtórzeń/sekund'
        }
