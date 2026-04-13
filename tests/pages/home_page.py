from playwright.sync_api import Page, expect


class HomePage:
    URL = "/home/"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        self.username_display = page.locator(".sidenav p")
        self.achievements_section = page.locator("h3:text('Osiągnięcia')")
        self.training_history = page.locator("h3:text('Historia treningów')")
        self.history_table = page.locator("table")
        self.stats_cards = page.locator(".card-body")

    def navigate(self):
        self.page.goto(self.base_url + self.URL)

    def is_on_home_page(self) -> bool:
        return self.page.url.endswith(self.URL) or "/home" in self.page.url

    def get_welcome_message(self) -> str:
        return self.username_display.first.text_content()

    def has_achievement(self, achievement_name: str) -> bool:
        achievement_locator = self.page.locator(f"strong:text('{achievement_name}')")
        return achievement_locator.count() > 0

    def has_training_in_history(self, exercise_name: str, value: str) -> bool:
        rows = self.history_table.locator("tbody tr")
        for row in rows.all():
            cells = row.locator("td")
            if cells.count() >= 3:
                exercise_cell = cells.nth(1).text_content()
                value_cell = cells.nth(2).text_content()
                if exercise_name in exercise_cell and value in value_cell:
                    return True
        return False
