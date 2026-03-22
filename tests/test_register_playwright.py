import uuid
import pytest
from playwright.sync_api import Page
from tests.pages.register_page import RegisterPage


def unique_username(prefix: str) -> str:
    """Unikalny username per run — zapobiega konfliktom w bazie."""
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


class TestFirstNameLength:

    def test_TC1_first_name_max_length_valid(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(first_name="A" * 30, username=unique_username("tc1"))
        rp.submit()
        assert rp.registration_succeeded(), \
            "TC1: imię o długości 30 znaków powinno przejść walidację"

    def test_TC2_first_name_min_length_valid(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(first_name="Ab", username=unique_username("tc2"))
        rp.submit()
        assert rp.registration_succeeded(), \
            "TC2: imię o długości 2 znaków powinno przejść walidację"

    def test_TC3_first_name_too_short(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(first_name="A", username=unique_username("tc3"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC3: imię 1-znakowe powinno zostać na stronie rejestracji"
        rp.expect_field_too_short("first_name")

    def test_TC4_first_name_too_long(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.remove_maxlength("first_name")
        rp.fill(first_name="A" * 31, username=unique_username("tc4"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC4: imię 31-znakowe powinno zostać na stronie rejestracji"
        rp.expect_errors_visible()


class TestFirstNameLettersOnly:

    def test_TC5_first_name_letters_only(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(first_name="Anna", username=unique_username("tc5"))
        rp.submit()
        assert rp.registration_succeeded(), \
            "TC5: imię złożone wyłącznie z liter powinno przejść walidację"

    def test_TC6_first_name_special_char(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(first_name="An@na", username=unique_username("tc6"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC6: imię ze znakiem '@' powinno zostać na stronie rejestracji"
        rp.expect_errors_visible()

    def test_TC7_first_name_digit(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(first_name="An1na", username=unique_username("tc7"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC7: imię z cyfrą powinno zostać na stronie rejestracji"
        rp.expect_errors_visible()

    def test_TC8_first_name_space(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(first_name="An na", username=unique_username("tc8"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC8: imię ze spacją powinno zostać na stronie rejestracji"
        rp.expect_errors_visible()


class TestLastNameLength:

    def test_TC9_last_name_max_length_valid(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(last_name="A" * 30, username=unique_username("tc9"))
        rp.submit()
        assert rp.registration_succeeded(), \
            "TC9: nazwisko o długości 30 znaków powinno przejść walidację"

    def test_TC10_last_name_too_long(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.remove_maxlength("last_name")
        rp.fill(last_name="A" * 31, username=unique_username("tc10"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC10: nazwisko 31-znakowe powinno zostać na stronie rejestracji"
        rp.expect_errors_visible()

    def test_TC11_last_name_min_length_valid(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(last_name="Ko", username=unique_username("tc11"))
        rp.submit()
        assert rp.registration_succeeded(), \
            "TC11: nazwisko o długości 2 znaków powinno przejść walidację"

    def test_TC12_last_name_too_short(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(last_name="K", username=unique_username("tc12"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC12: nazwisko 1-znakowe powinno zostać na stronie rejestracji"
        rp.expect_field_too_short("last_name")


class TestLastNameLettersOnly:

    def test_TC13_last_name_letters_only(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(last_name="Kowalski", username=unique_username("tc13"))
        rp.submit()
        assert rp.registration_succeeded(), \
            "TC13: nazwisko złożone wyłącznie z liter powinno przejść walidację"

    def test_TC14_last_name_special_char(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(last_name="Kowal$ki", username=unique_username("tc14"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC14: nazwisko ze znakiem '$' powinno zostać na stronie rejestracji"
        rp.expect_errors_visible()

    def test_TC15_last_name_digit(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(last_name="Kowal5ki", username=unique_username("tc15"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC15: nazwisko z cyfrą powinno zostać na stronie rejestracji"
        rp.expect_errors_visible()

    def test_TC16_last_name_space(self, page: Page, django_server):
        rp = RegisterPage(page, django_server)
        rp.navigate()
        rp.fill(last_name="Kowal ski", username=unique_username("tc16"))
        rp.submit()
        assert rp.is_on_register_page(), \
            "TC16: nazwisko ze spacją powinno zostać na stronie rejestracji"
        rp.expect_errors_visible()
