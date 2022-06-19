from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username





class Pushup(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add="True")
    pushups = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.user.person)
