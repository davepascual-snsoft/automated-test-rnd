import random
from typing import TypedDict
from playwright.sync_api import Page
from utils.combobox import select_combobox_option
from utils.input import fill_input


class CreateTablePitOptions(TypedDict):
    description: str
    code: str
    active: bool
    zone: str


class EditTablePitOptions(TypedDict):
    description: str
    code: str
    active: bool
    zone: str


class DeleteTablePitOptions(TypedDict):
    code: str


class TablePitPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, base_url: str):
        self.page.goto(base_url)

    def get_title(self) -> str:
        return self.page.title()

    def is_heading_visible(self) -> bool:
        return self.page.locator("h1").is_visible()

    def create_table_pit(self, **kwargs: CreateTablePitOptions):
        description: str = kwargs["description"]
        code: str = kwargs["code"]
        zone: str = kwargs["zone"]
        active: bool = kwargs["active"]

        self.fill_table_pit_description(description)
        self.fill_table_pit_code(code)
        self.fill_table_pit_zone(zone)
        self.fill_table_pit_status(active)
        self.click_save_table_pit_button()

    def click_add_table_pit_button(self):
        self.page.locator("button:has-text('Add Table Pit')").click()

    def fill_table_pit_description(self, description: str):
        self.page.locator("input[name='description']").fill(description)

    def fill_table_pit_code(self, code: str):
        self.page.locator("input[name='code']").fill(code)

    def fill_table_pit_zone(self, zone: str):
        select_combobox_option(page=self.page, label_text="Zone:", value=zone)

    def fill_table_pit_status(self, active: bool):
        value = "Active" if active else "Inactive"
        select_combobox_option(page=self.page, label_text="Status:", value=value)

    def click_save_table_pit_button(self):
        self.page.locator("button:has-text('Confirm')").click()

    def is_table_pit_created(self, **kwargs: CreateTablePitOptions) -> bool:
        description: str = kwargs["description"]
        code: str = kwargs["code"]

        self.search_table_pit(code)

        row = (
            self.page.locator("table tbody tr")
            .filter(has=self.page.locator(f"td:has-text('{description}')"))
            .filter(has=self.page.locator(f"td:has-text('{code}')"))
            .first
        )
        row.wait_for(state="visible", timeout=10_000)
        return row.is_visible()

    def click_edit_table_pit_button(self):
        table_body = self.page.locator("table[data-slot='table'] tbody")
        rows = table_body.locator("tr").all()
        selected_row = rows[random.randrange(0, len(rows))]
        if selected_row:
            selected_row.locator("button:has-text('Edit')").click()
        else:
            raise Exception("No table pit found")

    def edit_table_pit(self, **kwargs: EditTablePitOptions):
        description: str = kwargs["description"]
        code: str = kwargs["code"]
        zone: str = kwargs["zone"]
        active: bool = kwargs["active"]

        self.fill_table_pit_description(description)
        self.fill_table_pit_code(code)
        self.fill_table_pit_zone(zone)
        self.fill_table_pit_status(active)
        self.click_save_table_pit_button()

    def is_table_pit_edited(self, **kwargs: EditTablePitOptions) -> bool:
        description: str = kwargs["description"]
        code: str = kwargs["code"]

        self.search_table_pit(code)

        row = (
            self.page.locator("table tbody tr")
            .filter(has=self.page.locator(f"td:has-text('{description}')"))
            .filter(has=self.page.locator(f"td:has-text('{code}')"))
        )
        row.wait_for(state="visible", timeout=10_000)
        return row.is_visible()

    def click_delete_table_pit_button(self):
        table_body = self.page.locator("table[data-slot='table'] tbody")
        rows = table_body.locator("tr").all()
        selected_row = rows[random.randrange(0, len(rows))]
        if selected_row:
            selected_row.locator("button:has-text('Delete')").click()
        else:
            raise Exception("No table pit found")

    def delete_table_pit(self, **kwargs: DeleteTablePitOptions):
        code: str = kwargs["code"]

        row = self.page.locator("table tbody tr").filter(
            has=self.page.locator(f"td:has-text('{code}')")
        )
        row.wait_for(state="visible", timeout=10_000)
        row.locator("button:has-text('Delete')").click()

        delete_dialog = self.page.get_by_role("alertdialog")
        delete_dialog.wait_for(state="visible", timeout=10_000)
        delete_dialog.locator("button:has-text('Delete')").click()

    def is_table_pit_deleted(self, **kwargs: DeleteTablePitOptions) -> bool:
        code: str = kwargs["code"]
        self.search_table_pit(code)

        row = self.page.locator("table tbody tr").filter(
            has=self.page.locator(f"td:has-text('{code}')")
        )
        row.wait_for(state="hidden", timeout=10_000)
        return not row.is_visible()

    def search_table_pit(self, code: str):
        fill_input(page=self.page, placeholder="Search Table Pit Code", value=code)
        self.page.get_by_role("button", name="Search", exact=True).click()
        self.page.wait_for_load_state("networkidle")
