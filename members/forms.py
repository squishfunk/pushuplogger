from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from main.models import Person
import re

letters_only = RegexValidator(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+$', 'Pole może zawierać tylko litery.')

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, min_length=2, required=True, validators=[letters_only])
    last_name = forms.CharField(max_length=30, min_length=2, required=True, validators=[letters_only])
    username = forms.CharField(max_length=30, min_length=3, required=True)
    nickname = forms.CharField(max_length=30, min_length=3, required=False)
    age = forms.IntegerField(required=True, validators=[MinValueValidator(7), MaxValueValidator(100)])
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")

        if nickname and Person.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("There is a user witch such a nickname!")

        return nickname

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not password:
            return password

        if len(password) < 8:
            raise forms.ValidationError("This password is too short. It must contain at least 8 characters.")
        if len(password) > 64:
            raise forms.ValidationError("This password is too long.")

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase!")

        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase!")

        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number!")

        if not re.search(r'[^A-Za-z0-9]', password):
            raise forms.ValidationError("Password must contain at least one special character!")

        return password

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
