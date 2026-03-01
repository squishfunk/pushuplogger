from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class ExerciseType(models.Model):
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=20, default="powtórzenia")

    def __str__(self):
        return str(self.name)

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(default=0)
    
    # Statystyki Streak
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_log_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class ExerciseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    value = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type.name} - {self.date}"

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    target_value = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_icon = models.CharField(max_length=50, default="award")
    requirement_type = models.CharField(max_length=50) # np. 'total_reps', 'streak'
    requirement_value = models.IntegerField()

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

class Pushup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add="True")
    pushups = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.user.person)
