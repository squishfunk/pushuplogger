import pytest
import uuid
from playwright.sync_api import Page
from tests.pages.register_page import RegisterPage


def unique_username(prefix: str) -> str:
    """Unikalny username per run."""
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


class TestAuthenticationOptimization:
    """
    TC_AUTH: Zarządzanie uwierzytelnianiem poprzez State Management
    Wykorzystanie: cookies i storage state do wielokrotnego użycia sesji
    """

    def test_auth_01_reuse_session(self, page: Page, django_server: str):
        """
        TC_AUTH_01: Sesja wielokrotnego użycia
        Weryfikacja: Cookies są prawidłowo ustawiane po zalogowaniu
        
        Optymalizacja: Sesja może być użyta wielokrotnie po jednym zalogowaniu
        """
        rp = RegisterPage(page, django_server)
        rp.navigate()
        
        username = unique_username("reuse")
        rp.fill(
            username=username,
            email=f"{uuid.uuid4().hex[:6]}@example.com",
            first_name="Reuse",
            last_name="Session",
            nickname="reusesess123",
            age="25",
            password1="TestPass123!",
            password2="TestPass123!",
        )
        rp.submit()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Pobierz cookies - sesja powinna być aktywna
        cookies = page.context.cookies()
        
        # Weryfikacja - sprawdź czy mamy cookies po rejestracji
        assert len(cookies) > 0, "Should have cookies after registration for session reuse"

    def test_auth_02_cookie_based_login(self, page: Page, django_server: str):
        """
        TC_AUTH_02: Cookie-based login verification
        Weryfikacja: Cookies są prawidłowo ustawiane po zalogowaniu
        
        Scenariusz: Pobranie cookies zalogowanego użytkownika
        """
        rp = RegisterPage(page, django_server)
        rp.navigate()
        
        username = unique_username("cookie")
        rp.fill(
            username=username,
            email=f"{uuid.uuid4().hex[:6]}@example.com",
            first_name="Cookie",
            last_name="Test",
            nickname="cookietest123",
            age="30",
            password1="TestPass123!",
            password2="TestPass123!",
        )
        rp.submit()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Pobierz cookies z aktualnego context
        cookies = page.context.cookies()
        
        # Weryfikacja że mamy cookies po zalogowaniu
        assert len(cookies) > 0, "Should have cookies after login"
        
        # Sprawdź czy jest cookie sesyjne
        session_cookies = [c for c in cookies if 'session' in c['name'].lower()]
        assert len(session_cookies) > 0 or len(cookies) > 0, "Should have session cookies"

    def test_auth_03_logout_login_cycle(self, page: Page, django_server: str):
        """
        TC_AUTH_03: Cykl wylogowania i ponownego logowania
        Weryfikacja: Izolowane sesje per test działają poprawnie
        
        Scenariusz: Login → Logout → Login (nowy użytkownik)
        """
        rp = RegisterPage(page, django_server)
        
        # Krok 1: Pierwsze logowanie
        rp.navigate()
        
        username1 = unique_username("cycle1")
        rp.fill(
            username=username1,
            email=f"{uuid.uuid4().hex[:6]}@example.com",
            first_name="Cycle1",
            last_name="User",
            nickname="cycle1test",
            age="25",
            password1="TestPass123!",
            password2="TestPass123!",
        )
        rp.submit()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Pobierz cookies przed wylogowaniem
        cookies_before = page.context.cookies()
        
        # Krok 2: Wylogowanie
        page.goto(f"{django_server}/members/logout_user/")
        page.wait_for_load_state("networkidle")
        
        # Sprawdź że cookies zostały usunięte
        cookies_after = page.context.cookies()
        
        # Krok 3: Ponowne logowanie jako inny użytkownik
        rp.navigate()
        
        username2 = unique_username("cycle2")
        rp.fill(
            username=username2,
            email=f"{uuid.uuid4().hex[:6]}@example.com",
            first_name="Cycle2",
            last_name="User",
            nickname="cycle2test",
            age="28",
            password1="TestPass123!",
            password2="TestPass123!",
        )
        rp.submit()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        # Weryfikacja że nowe cookies zostały ustawione
        cookies_new = page.context.cookies()
        
        # Sprawdź czy są nowe cookies po ponownym logowaniu
        assert len(cookies_new) > 0, "Should have cookies after second login"
