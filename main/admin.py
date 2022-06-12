from django.contrib import admin
from .models import Person
from .models import Pushup

#admin.site.register(Person)
#admin.site.register(Pushup)

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'id', 'age')
    search_fields = ('name', 'id', 'age')

@admin.register(Pushup)
class PushupAdmin(admin.ModelAdmin):
    list_display = ('person', 'date', 'pushups')
    search_fields = ('name', 'date')
# Register your models here.
