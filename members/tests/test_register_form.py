from django.contrib.auth import get_user_model
from django.test import TestCase

from main.models import Person
from ..forms import RegisterForm

# Funkcja do danych mockowych
def valid_data(**overrides):
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Jan",
        "last_name": "Kowalski",
        "nickname": "janek",
        "age": 25,
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
    }
    data.update(overrides)
    return data


class FirstNameLengthTest(TestCase):

    def test_TC1_first_name_max_length_valid(self):
        form = RegisterForm(data=valid_data(first_name="A" * 30))
        self.assertTrue(form.is_valid())

    def test_TC2_first_name_min_length_valid(self):
        form = RegisterForm(data=valid_data(first_name="Ab"))
        self.assertTrue(form.is_valid())

    def test_TC3_first_name_too_short(self):
        form = RegisterForm(data=valid_data(first_name="A"))
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_TC4_first_name_too_long(self):
        form = RegisterForm(data=valid_data(first_name="A" * 31))
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)


class FirstNameLettersOnlyTest(TestCase):
    def test_TC5_first_name_letters_only(self):
        form = RegisterForm(data=valid_data(first_name="Anna"))
        self.assertTrue(form.is_valid())

    def test_TC6_first_name_special_char(self):
        form = RegisterForm(data=valid_data(first_name="An@na"))
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_TC7_first_name_digit(self):
        form = RegisterForm(data=valid_data(first_name="An1na"))
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)

    def test_TC8_first_name_space(self):
        form = RegisterForm(data=valid_data(first_name="An na"))
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)


class LastNameLengthTest(TestCase):
    def test_TC9_last_name_max_length_valid(self):
        form = RegisterForm(data=valid_data(last_name="A" * 30))
        self.assertTrue(form.is_valid())

    def test_TC10_last_name_too_long(self):
        form = RegisterForm(data=valid_data(last_name="A" * 31))
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_TC11_last_name_min_length_valid(self):
        form = RegisterForm(data=valid_data(last_name="Ko"))
        self.assertTrue(form.is_valid())

    def test_TC12_last_name_too_short(self):
        form = RegisterForm(data=valid_data(last_name="K"))
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)


class LastNameLettersOnlyTest(TestCase):
    def test_TC13_last_name_letters_only(self):
        form = RegisterForm(data=valid_data(last_name="Kowalski"))
        self.assertTrue(form.is_valid())

    def test_TC14_last_name_special_char(self):
        form = RegisterForm(data=valid_data(last_name="Kowal$ki"))
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_TC15_last_name_digit(self):
        form = RegisterForm(data=valid_data(last_name="Kowal5ki"))
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_TC16_last_name_space(self):
        form = RegisterForm(data=valid_data(last_name="Kowal ski"))
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)


class PasswordValidationTest(TestCase):

    def test_TC17_password_all_criteria_met(self):
        form = RegisterForm(data=valid_data(password1="Haslo123!", password2="Haslo123!"))
        self.assertTrue(form.is_valid())

    def test_TC18_password_missing_uppercase(self):
        form = RegisterForm(data=valid_data(password1="haslo123!", password2="haslo123!"))
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_TC19_password_missing_lowercase(self):
        form = RegisterForm(data=valid_data(password1="HASLO123!", password2="HASLO123!"))
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_TC20_password_missing_special_char(self):
        form = RegisterForm(data=valid_data(password1="Haslo123", password2="Haslo123"))
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_TC21_password_missing_digit(self):
        form = RegisterForm(data=valid_data(password1="Haslo!!!", password2="Haslo!!!"))
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_TC22_password_too_short(self):
        form = RegisterForm(data=valid_data(password1="Ab1!", password2="Ab1!"))
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)

    def test_TC23_password_exactly_8_chars(self):
        form = RegisterForm(data=valid_data(password1="Abcde12!", password2="Abcde12!"))
        self.assertTrue(form.is_valid())

    def test_TC24_password_exactly_64_chars(self):
        form = RegisterForm(data=valid_data(password1="Abcde12!" + "a" * 56, password2="Abcde12!" + "a" * 56))
        self.assertTrue(form.is_valid())

    def test_TC25_password_too_long(self):
        form = RegisterForm(data=valid_data(password1="a" * 65, password2="a" * 65))
        self.assertFalse(form.is_valid())
        self.assertIn("password1", form.errors)


class UsernameValidationTest(TestCase):

    def test_TC26_username_max_length_30(self):
        form = RegisterForm(data=valid_data(username="u" * 30))
        self.assertTrue(form.is_valid())

    def test_TC27_username_over_30_chars(self):
        form = RegisterForm(data=valid_data(username="u" * 31))
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_TC28_username_min_length_3(self):
        form = RegisterForm(data=valid_data(username="abc"))
        self.assertTrue(form.is_valid())

    def test_TC29_username_under_3_chars(self):
        form = RegisterForm(data=valid_data(username="ab"))
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_TC30_username_existing_in_db(self):
        from django.contrib.auth.models import User
        User.objects.create_user(username="testadmin", password="TestPass123!")
        form = RegisterForm(data=valid_data(username="testadmin"))
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_TC31_username_new_unique(self):
        form = RegisterForm(data=valid_data(username="user123"))
        self.assertTrue(form.is_valid())


class NicknameValidationTest(TestCase):

    def test_TC32_nickname_empty(self):
        form = RegisterForm(data=valid_data(nickname=""))
        self.assertTrue(form.is_valid())

    def test_TC33_nickname_max_length_30(self):
        form = RegisterForm(data=valid_data(nickname="n" * 30))
        self.assertTrue(form.is_valid())

    def test_TC34_nickname_min_length_3(self):
        form = RegisterForm(data=valid_data(nickname="abc"))
        self.assertTrue(form.is_valid())

    def test_TC35_nickname_under_3_chars(self):
        form = RegisterForm(data=valid_data(nickname="ab"))
        self.assertFalse(form.is_valid())
        self.assertIn("nickname", form.errors)

    def test_TC36_nickname_over_30_chars(self):
        form = RegisterForm(data=valid_data(nickname="n" * 31))
        self.assertFalse(form.is_valid())
        self.assertIn("nickname", form.errors)

    def test_TC37_nickname_existing_in_db(self):
        User = get_user_model()
        new_user = User.objects.create_user(username="testadmin_user", password="TestPass123!")
        Person.objects.create(
            user=new_user,
            nickname="testadmin",
            name="Test",
            surname="Admin"
        )
        form = RegisterForm(data=valid_data(nickname="testadmin"))
        self.assertFalse(form.is_valid())
        self.assertIn("nickname", form.errors)

    def test_TC38_nickname_new_unique(self):
        form = RegisterForm(data=valid_data(nickname="user123"))
        self.assertTrue(form.is_valid())


class AgeValidationTest(TestCase):

    def test_TC39_age_max_100(self):
        form = RegisterForm(data=valid_data(age=100))
        self.assertTrue(form.is_valid())

    def test_TC40_age_over_100(self):
        form = RegisterForm(data=valid_data(age=101))
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)

    def test_TC41_age_min_7(self):
        form = RegisterForm(data=valid_data(age=7))
        self.assertTrue(form.is_valid())

    def test_TC42_age_under_7(self):
        form = RegisterForm(data=valid_data(age=6))
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)

    def test_TC43_age_as_integer(self):
        form = RegisterForm(data=valid_data(age=50))
        self.assertTrue(form.is_valid())

    def test_TC44_age_as_float(self):
        form = RegisterForm(data=valid_data(age=50.5))
        self.assertFalse(form.is_valid())
        self.assertIn("age", form.errors)
