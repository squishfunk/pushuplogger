from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .models import Pushup
from .forms import Addnewlog
import calendar
from calendar import HTMLCalendar
from django.db.models import Sum, Count
import datetime as DT

def viewcalendar(request,year, month):
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)
    return render(request, 'main/calendar.html',{
        "year":year,
        "month":month,
        "cal":cal,
    })
def view1(response):
    return render(response, 'main/base.html', {})

def viewhome(response):
    return render(response, 'main/home.html', {})

def viewmylogs(response):
    return render(response, 'main/calendar.html', {})

def viewnewlog(request):

    submitted = False
    if request.method == "POST":


        if Pushup.objects.filter(person=request.POST.get('person'),date__gte=DT.date.today() - DT.timedelta(days=1)).exists():
            return HttpResponseBadRequest("Błąd: Rekord danego użytkownika został już dzisiaj dodany")
        form = Addnewlog(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/newlog?submitted=True")
    else:
        #
        form = Addnewlog
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'main/newlog.html', {"form":form, 'submitted':submitted})

def viewtop5(request):

    top5_list = Pushup.objects.filter(date__gte=DT.date.today()-DT.timedelta(days=7)).values('person_id__name','person_id__surname').annotate(totalpushups=Sum('pushups')).order_by('-totalpushups')[:5]

    return render(request, 'main/top5.html', {'top5_list': top5_list})

def viewtop3(request):

    top3_list = Pushup.objects.filter(date__gte=DT.date.today()-DT.timedelta(days=30)).values('person_id__name','person_id__surname').annotate(totalseries=Count('pushups')).order_by('-totalseries')[:3]

    return render(request, 'main/top3.html', {'top3_list': top3_list})

# Create your views here.
