from django.urls import path
from . import views

urlpatterns = [
    path("", views.viewhome, name="home"),
    path("home/", views.viewhome, name="home"),
    path('<int:year>/<str:month>/',views.viewcalendar, name='calendar'),
    path("newlog/", views.viewnewlog, name="newlog"),
    path("top5/", views.viewtop5, name="top5"),
    path("top3/", views.viewtop3, name="top3"),

]