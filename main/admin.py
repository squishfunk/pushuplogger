from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Pushup, Person

class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = 'People'

class CustomUserAdmin(UserAdmin):
    inlines = (PersonInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Pushup)
class PushupAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'pushups')
    search_fields = ('name', 'date')

