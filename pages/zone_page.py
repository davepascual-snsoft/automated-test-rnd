import random
from playwright.sync_api import Page
from utils.combobox import select_combobox_option


class ZonePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, base_url: str):
        self.page.goto(base_url)

    def get_title(self) -> str:
        return self.page.title()

    def is_heading_visible(self) -> bool:
        return self.page.locator("h1").is_visible()

    def create_zone(self, description: str, code: str, cage: str, active: bool):
        self.fill_zone_description(description)
        self.fill_zone_code(code)
        self.fill_zone_cage(cage)
        self.fill_zone_status(active)
        self.click_save_zone_button()

    def click_add_zone_button(self):
        self.page.locator("button:has-text('Add Zone')").click()

    def fill_zone_description(self, description: str):
        self.page.locator("textarea[name='description']").fill(description)

    def fill_zone_code(self, code: str):
        self.page.locator("input[name='code']").fill(code)

    def fill_zone_cage(self, cage: str):
        select_combobox_option(page=self.page, label_text="Cage:", value=cage)

    def fill_zone_status(self, active: bool):
        value = "Active" if active else "Inactive"
        select_combobox_option(page=self.page, label_text="Status:", value=value)

    def click_save_zone_button(self):
        self.page.locator("button:has-text('Confirm')").click()

    def is_zone_created(self, description: str) -> bool:
        return self.page.locator(f"table:has-text('{description}')").is_visible()

    def click_edit_zone_button(self):
        table_body = self.page.locator("table[data-slot='table'] tbody")
        rows = table_body.locator("tr").all()
        selected_row =  rows[random.randrange(0, len(rows))]
        if selected_row:
            selected_row.locator("button:has-text('Edit')").click()
        else:
            raise Exception("No zone found")

    def edit_zone(self, description: str, code: str, cage: str, active: bool):
        self.fill_zone_description(description)
        self.fill_zone_code(code)
        self.fill_zone_cage(cage)
        self.fill_zone_status(active)
        self.click_save_zone_button()
    