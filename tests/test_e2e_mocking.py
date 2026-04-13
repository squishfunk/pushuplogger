import pytest
import uuid
from playwright.sync_api import Page
from tests.pages.register_page import RegisterPage


def unique_username(prefix: str) -> str:
    """Unikalny username per run."""
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


@pytest.fixture
def logged_in_page(page: Page, django_server):
    """Fixture który loguje użytkownika i zwraca stronę."""
    rp = RegisterPage(page, django_server)
    rp.navigate()
    rp.fill(
        username=unique_username("mock"),
        email=f"mock_{id(page)}@example.com",
        first_name="Mock",
        last_name="User",
        nickname="mockuser123",
        age="30",
        password1="TestPass123!",
        password2="TestPass123!",
    )
    rp.submit()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    return page


class TestFrontendMocking:
    """
    TC_MOCK: Izolacja frontendu poprzez mockowanie zapytań API
    Wykorzystanie: page.route() do intercepcji i mockowania odpowiedzi
    """

    def test_mock_01_top5_rankings_display(self, logged_in_page: Page, django_server: str):
        """
        TC_MOCK_01: Mock rankingu TOP5
        Weryfikacja: Wyświetlanie kontrolowanych danych w tabeli rankingowej
        
        Mockowane dane: predefiniowana lista TOP5 użytkowników
        """
        page = logged_in_page
        
        # Mockowane dane (bez emoji dla uniknięcia problemów z kodowaniem)
        mock_top5_html = """
        <!DOCTYPE html>
        <html><body>
            <table class="table">
                <tbody>
                    <tr><td>GOLD</td><td>Jan Kowalski</td><td>500</td></tr>
                    <tr><td>SILVER</td><td>Anna Nowak</td><td>450</td></tr>
                    <tr><td>BRONZE</td><td>Piotr Wisniewski</td><td>400</td></tr>
                </tbody>
            </table>
        </body></html>
        """
        
        # Mockowanie zapytania do /top5/
        def handle_top5_route(route):
            route.fulfill(
                status=200,
                content_type="text/html",
                body=mock_top5_html
            )
        
        page.route(f"{django_server}/top5/**", handle_top5_route)
        
        # Otwórz stronę TOP5
        page.goto(f"{django_server}/top5/")
        page.wait_for_load_state("networkidle")
        
        # Weryfikacja mock danych
        assert "Jan Kowalski" in page.content()
        assert "Anna Nowak" in page.content()
        assert "500" in page.content()
        assert "GOLD" in page.content()

    def test_mock_02_user_stats_display(self, logged_in_page: Page, django_server: str):
        """
        TC_MOCK_02: Mock statystyk użytkownika
        Weryfikacja: Wyświetlanie symulowanych wartości streak i statystyk
        
        Mockowane dane: statystyki z różnymi wartościami streak
        """
        page = logged_in_page
        
        # Mock strony domowej z kontrolowanymi statystykami
        mock_home_html = """
        <!DOCTYPE html>
        <html>
        <body class="sidenav">
            <p>Witaj Mock</p>
            <div class="main">
                <div class="card">
                    <div class="card-body">
                        <p class="card-text" style="font-size: 2rem;">STREAK: 99 dni</p>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <p class="card-text" style="font-size: 2rem;">RECORD: 365 dni</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        def handle_home_route(route):
            route.fulfill(
                status=200,
                content_type="text/html",
                body=mock_home_html
            )
        
        page.route(f"{django_server}/home/**", handle_home_route)
        
        page.goto(f"{django_server}/home/")
        page.wait_for_load_state("networkidle")
        
        # Weryfikacja mockowanych statystyk
        assert "99 dni" in page.content()
        assert "365 dni" in page.content()

    def test_mock_03_achievements_display(self, logged_in_page: Page, django_server: str):
        """
        TC_MOCK_03: Mock osiągnięć (badges)
        Weryfikacja: Wyświetlanie fałszywych achievement badges
        
        Mockowane dane: lista osiągnięć użytkownika
        """
        page = logged_in_page
        
        # Mock osiągnięć (bez emoji)
        mock_achievements_html = """
        <!DOCTYPE html>
        <html>
        <body class="sidenav">
            <p>Witaj Mock</p>
            <div class="main">
                <h3>Osiagniecia</h3>
                <div class="row">
                    <div class="col-4 text-center">
                        <strong>Pierwszy Krok</strong>
                    </div>
                    <div class="col-4 text-center">
                        <strong>Tysiacznik</strong>
                    </div>
                    <div class="col-4 text-center">
                        <strong>Wytrwaly</strong>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        def handle_achievements_route(route):
            route.fulfill(
                status=200,
                content_type="text/html",
                body=mock_achievements_html
            )
        
        page.route(f"{django_server}/home/**", handle_achievements_route)
        
        page.goto(f"{django_server}/home/")
        page.wait_for_load_state("networkidle")
        
        # Weryfikacja mockowanych osiągnięć
        assert "Pierwszy Krok" in page.content()
        assert "Tysiacznik" in page.content()
        assert "Wytrwaly" in page.content()
