from django import forms
from django.forms import ModelForm
from .models import Person, Pushup

class Addnewlog(ModelForm):
    class Meta:
        model = Pushup
        fields = ('person', 'pushups')

