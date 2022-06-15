from django import forms
from django.forms import ModelForm
from .models import Pushup

class Addnewlog(ModelForm):
    class Meta:
        model = Pushup
        fields = ("pushups",)

#<a href="{% url 'calendar' year month %}">Kalendarz</a>-