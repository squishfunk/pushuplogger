from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from main.models import Person

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    nickname = forms.CharField(max_length=30, required=False)
    age = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            Person.objects.create(
                user=user,
                name=self.cleaned_data["first_name"],
                surname=self.cleaned_data["last_name"],
                nickname=self.cleaned_data.get("nickname", ""),
                age=self.cleaned_data["age"]
            )
        return user
