from django.forms import ModelForm
from .models import Pushup

class Addnewlog(ModelForm):
    class Meta:
        model = Pushup
        fields = ("pushups",)

