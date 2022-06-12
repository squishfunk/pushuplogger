from django.db import models

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(default=0)


    def __str__(self):
        return self.name + ' ' + self.surname


class Pushup(models.Model):

    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add="True")
    pushups = models.IntegerField(default=0)

    def __str__(self):
        return str(self.person)
