from playwright.sync_api import Page, expect


class NewLogPage:
    URL = "/newlog/"

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

        self.exercise_type_select = page.locator("select#id_exercise_type")
        self.value_input = page.locator("input#id_value")
        self.submit_button = page.locator("input[type=submit]")
        self.success_message = page.locator("p:text('Twój rekord został dodany pomyślnie')")

    def navigate(self):
        self.page.goto(self.base_url + self.URL)
        self.page.wait_for_load_state("domcontentloaded")

    def is_on_newlog_page(self) -> bool:
        return self.page.url.endswith(self.URL) or "/newlog" in self.page.url

    def fill_form(self, exercise_type: str = None, value: str = "50"):
        if value:
            self.value_input.wait_for(state="visible", timeout=10000)
            self.value_input.fill(value)
        if exercise_type is not None:
            self.exercise_type_select.select_option(label=exercise_type)

    def submit(self):
        self.submit_button.click()

    def is_submission_successful(self) -> bool:
        return self.success_message.count() > 0
