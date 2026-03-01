from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .models import ExerciseLog, ExerciseType, Goal, Achievement, UserAchievement
from django.contrib.auth.decorators import login_required
from .forms import Addnewlog
import calendar
from calendar import HTMLCalendar
from django.db.models import Sum, Count
import datetime as dt

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .services import update_user_stats

@login_required
def viewpdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    text = c.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Helvetica", 12)

    lines = []
    records = ExerciseLog.objects.filter(user=request.user).order_by('-date')
    current_user = f"{request.user.person.name} {request.user.person.surname}"
    lines.append(current_user)
    lines.append(" ")

    for record in records:
        record_summary = f"Data: {record.date} | {record.exercise_type.name}: {record.value}"
        lines.append(record_summary)

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="Moje rekordy.pdf")

def viewcalendar(request, year, month):
    month = month.title()
    datenow = dt.date.today()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)
    return render(request, 'main/calendar.html', {
        "year":year,
        "month":month,
        "cal":cal,
        "datenow":datenow
    })

def viewmainpage(response):
    datenow = dt.date.today()
    month = datenow.strftime("%B")
    year = datenow.year

    return render(response, 'main/mainpage.html', {
        "year": year,
        "month": month,
    })

@login_required
def viewhome(request):
    myrecord_list = ExerciseLog.objects.filter(user=request.user).order_by('-date')
    stats = request.user.person
    achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')
    goals = Goal.objects.filter(user=request.user)

    return render(request, 'main/home.html', {
        'myrecord_list': myrecord_list,
        'stats': stats,
        'achievements': achievements,
        'goals': goals
    })

@login_required
def viewnewlog(request):
    submitted = False
    if request.method == "POST":
        # Sprawdzamy zasadę 1 wpisu dziennie
        if ExerciseLog.objects.filter(user=request.user, date=dt.date.today()).exists():
            return HttpResponseBadRequest("Błąd: Rekord na dzisiaj został już dodany. Możesz dodać tylko jeden wpis dziennie.")

        form = Addnewlog(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()

            # Aktualizacja statystyk i osiągnięć
            update_user_stats(request.user)

            # Wysyłka maila
            template = render_to_string('main/emailtemplate.html', {
                'name': request.user.person.name, 
                'exercise': log.exercise_type.name,
                'value': log.value,
            })

            email = EmailMessage(
                'LOGGER: Dodano nowy rekord',
                template,
                settings.EMAIL_HOST_USER,
                [request.user.email],
            )
            email.send(fail_silently=True)

            return HttpResponseRedirect("/newlog?submitted=True")
    else:
        form = Addnewlog()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'main/newlog.html', {"form": form, 'submitted': submitted})

def viewtop5(request):
    # Ranking sumaryczny wszystkich ćwiczeń z ostatnich 7 dni
    top5_list = ExerciseLog.objects.filter(date__gte=dt.date.today()-dt.timedelta(days=7)).values('user__person__name', 'user__person__surname').annotate(totalvalue=Sum('value')).order_by('-totalvalue')[:5]
    return render(request, 'main/top5.html', {'top5_list': top5_list})

def viewtop3(request):
    # Ranking regularności z ostatnich 30 dni
    top3_list = ExerciseLog.objects.filter(date__gte=dt.date.today()-dt.timedelta(days=30)).values('user__person__name', 'user__person__surname').annotate(totalseries=Count('id')).order_by('-totalseries')[:3]
    return render(request, 'main/top3.html', {'top3_list': top3_list})
