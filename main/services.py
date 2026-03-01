from datetime import date, timedelta
from django.db.models import Sum
from .models import ExerciseLog, UserAchievement, Achievement, Goal

def update_user_stats(user):
    person = user.person
    today = date.today()
    
    # 1. Logika Streaks
    if person.last_log_date:
        if person.last_log_date == today - timedelta(days=1):
            person.current_streak += 1
        elif person.last_log_date < today - timedelta(days=1):
            person.current_streak = 1
        # Jeśli ostatni log był dzisiaj, nie zmieniamy streaka
    else:
        person.current_streak = 1
        
    person.last_log_date = today
    if person.current_streak > person.longest_streak:
        person.longest_streak = person.current_streak
    person.save()

    # 2. Logika Osiągnięć
    total_reps = ExerciseLog.objects.filter(user=user).aggregate(Sum('value'))['value__sum'] or 0
    
    potential_achievements = Achievement.objects.exclude(
        id__in=UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
    )
    
    for ach in potential_achievements:
        if ach.requirement_type == 'total_reps' and total_reps >= ach.requirement_value:
            UserAchievement.objects.create(user=user, achievement=ach)
        elif ach.requirement_type == 'streak' and person.current_streak >= ach.requirement_value:
            UserAchievement.objects.create(user=user, achievement=ach)

    # 3. Logika Celów
    active_goals = Goal.objects.filter(user=user, is_completed=False)
    for goal in active_goals:
        progress = ExerciseLog.objects.filter(
            user=user, 
            exercise_type=goal.exercise_type,
            date__range=[goal.start_date, goal.end_date]
        ).aggregate(Sum('value'))['value__sum'] or 0
        
        if progress >= goal.target_value:
            goal.is_completed = True
            goal.save()
