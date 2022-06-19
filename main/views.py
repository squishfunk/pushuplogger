from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .models import Pushup
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

def viewpdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    text = c.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Helvetica", 12)

    lines = []
    records = Pushup.objects.filter(user=request.user)
    current_user = request.user.person.name + ' ' + request.user.person.surname
    lines.append(current_user)
    lines.append(" ")

    for record in records:
        record_summary = "Data: " + str(record.date) + ' ' + "Wynik: " +  str(record.pushups)
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


def view1(response):
    return render(response, 'main/base.html', {})


def viewmainpage(response):
    datenow = dt.date.today()
    month = datenow.strftime("%B")
    year = datenow.year

    return render(response, 'main/mainpage.html', {
        "year": year,
        "month": month,
    })

def viewhome(request):

    myrecord_list = Pushup.objects.filter(user=request.user)

    return render(request, 'main/home.html', {'myrecord_list': myrecord_list})

def viewmylogs(response):

    return render(response, 'main/calendar.html', {})


@login_required
def viewnewlog(request):

    submitted = False
    if request.method == "POST":


        if Pushup.objects.filter(user=request.user,date__gte=dt.date.today() - dt.timedelta(days=1)).exists():
            return HttpResponseBadRequest("Błąd: Rekord danego użytkownika został już dzisiaj dodany")

        form = Addnewlog(request.POST)

        if form.is_valid():
            PushupForm = form.save(commit=False)
            PushupForm.user = request.user
            PushupForm.save()

            template = render_to_string('main/emailtemplate.html', {'name':request.user.person.name, 'pushups':PushupForm.pushups,})

            email = EmailMessage(
                'LOGGER POMPEK: Dodano rekord',
                template,
                settings.EMAIL_HOST_USER,
                [request.user.email],
            )

            email.fail_silently = False
            email.send()

            return HttpResponseRedirect("/newlog?submitted=True")
    else:

        form = Addnewlog

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'main/newlog.html', {"form": form, 'submitted': submitted})


def viewtop5(request):

    top5_list = Pushup.objects.filter(date__gte=dt.date.today()-dt.timedelta(days=7)).values('user__person__name', 'user__person__surname').annotate(totalpushups=Sum('pushups')).order_by('-totalpushups')[:5]

    return render(request, 'main/top5.html', {'top5_list': top5_list})


def viewtop3(request):

    top3_list = Pushup.objects.filter(date__gte=dt.date.today()-dt.timedelta(days=30)).values('user__person__name', 'user__person__surname').annotate(totalseries=Count('pushups')).order_by('-totalseries')[:3]

    return render(request, 'main/top3.html', {'top3_list': top3_list})

