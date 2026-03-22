from playwright.sync_api import Page, expect


class RegisterPage:
    URL = "/members/register_user"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        self.username_input   = page.locator("#id_username")
        self.email_input      = page.locator("#id_email")
        self.first_name_input = page.locator("#id_first_name")
        self.last_name_input  = page.locator("#id_last_name")
        self.nickname_input   = page.locator("#id_nickname")
        self.age_input        = page.locator("#id_age")
        self.password1_input  = page.locator("#id_password1")
        self.password2_input  = page.locator("#id_password2")
        self.submit_button    = page.locator("button[type=submit]")
        self.error_messages   = page.locator(".text-danger")

    def navigate(self):
        self.page.goto(self.base_url + self.URL)

    def fill(
        self,
        username: str   = "testuser",
        email: str       = "test@example.com",
        first_name: str  = "Jan",
        last_name: str   = "Kowalski",
        nickname: str    = "janek",
        age: str         = "25",
        password1: str   = "StrongPass123!",
        password2: str   = "StrongPass123!",
    ):
        self.username_input.fill(username)
        self.email_input.fill(email)
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.nickname_input.fill(nickname)
        self.age_input.fill(age)
        self.password1_input.fill(password1)
        self.password2_input.fill(password2)

    def submit(self):
        self.submit_button.click()

    def remove_maxlength(self, field: str):
        """Usuwa atrybut maxlength z pola (by wymusić walidację serwera)."""
        self.page.evaluate(
            f"document.getElementById('id_{field}').removeAttribute('maxlength')"
        )

    def is_on_register_page(self) -> bool:
        return (
            self.page.url.startswith(self.base_url + self.URL)
            or "register" in self.page.url
        )

    def registration_succeeded(self) -> bool:
        return not self.is_on_register_page()

    def expect_errors_visible(self):
        expect(self.error_messages).to_be_visible()

    def expect_field_too_short(self, field: str):
        is_invalid = self.page.evaluate(
            f"document.getElementById('id_{field}').validity.tooShort"
        )
        assert is_invalid, f"Pole '{field}' powinno być browser-invalid (tooShort)"
