import uuid
import pytest
from playwright.sync_api import Page, expect
from tests.pages.register_page import RegisterPage
from tests.pages.home_page import HomePage
from tests.pages.newlog_page import NewLogPage


def unique_username(prefix: str) -> str:
    """Unikalny username per run — zapobiega konfliktom w bazie."""
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


@pytest.fixture
def authenticated_page(page: Page, django_server):
    """Rejestruje użytkownika i zwraca zalogowaną stronę."""
    rp = RegisterPage(page, django_server)
    rp.navigate()
    rp.fill(
        username=unique_username("e2e"),
        email=f"e2e_{uuid.uuid4().hex[:6]}@example.com",
        first_name="Jan",
        last_name="Testowy",
        nickname="jantek123",
        age="30",
        password1="TestPass123!",
        password2="TestPass123!",
    )
    rp.submit()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    
    if "/register" in page.url or "/login" in page.url:
        print(f"Registration failed! Current URL: {page.url}")
        print(f"Page content: {page.content()[:500]}")
    
    return page


class TestUserRegistrationAndTraining:

    def test_e2e_01_user_registration(self, page: Page, django_server: str):
        rp = RegisterPage(page, django_server)
        home = HomePage(page, django_server)
        
        rp.navigate()
        
        username = unique_username("reg")
        rp.fill(
            username=username,
            email=f"reg_{uuid.uuid4().hex[:6]}@example.com",
            first_name="Anna",
            last_name="Kowalska",
            nickname="anakow123",
            age="25",
            password1="TestPass123!",
            password2="TestPass123!",
        )
        
        rp.submit()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        
        print(f"URL after registration: {page.url}")
        
        # Navigate to home
        home.navigate()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        if "/login" in page.url:
            page.screenshot(path="login_required.png")
            pytest.fail("User was not logged in after registration")
        
        welcome_text = home.get_welcome_message()
        assert "Anna" in welcome_text, \
            "Użytkownik powinien widzieć swoje imię 'Anna' w pasku bocznym"

    def test_e2e_02_add_training_and_history(self, authenticated_page: Page, django_server: str):
        page = authenticated_page
        newlog = NewLogPage(page, django_server)
        home = HomePage(page, django_server)
        
        test_value = "50"
        test_exercise = "Pompki"
        
        newlog.navigate()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        print(f"Newlog URL: {page.url}")
        
        newlog.fill_form(exercise_type=test_exercise, value=test_value)
        newlog.submit()
        page.wait_for_load_state("networkidle")
        
        home.navigate()
        page.wait_for_load_state("networkidle")
        
        assert home.has_training_in_history(test_exercise, test_value), \
            f"Historia treningów powinna zawierać wpis: {test_exercise} - {test_value}"

    def test_e2e_03_full_user_journey_with_achievement(self, authenticated_page: Page, django_server: str):
        page = authenticated_page
        base_url = django_server
        
        home = HomePage(page, base_url)
        newlog = NewLogPage(page, base_url)
        
        home.navigate()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        welcome_text = home.get_welcome_message()
        assert "Jan" in welcome_text, \
            "Użytkownik powinien widzieć swoje imię 'Jan' w pasku bocznym"
        
        newlog.navigate()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        test_value = "100"
        test_exercise = "Pompki"
        newlog.fill_form(exercise_type=test_exercise, value=test_value)
        newlog.submit()
        page.wait_for_load_state("networkidle")
        
        home.navigate()
        page.wait_for_load_state("networkidle")
        
        assert home.has_training_in_history(test_exercise, test_value), \
            f"Historia treningów powinna zawierać wpis: {test_exercise} - {test_value}"
        
        assert home.has_achievement("Pierwszy krok"), \
            "Użytkownik powinien mieć osiągnięcie 'Pierwszy krok' po dodaniu pierwszego treningu"
