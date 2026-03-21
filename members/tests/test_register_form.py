from django.test import TestCase
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
