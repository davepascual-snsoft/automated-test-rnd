from datetime import date
from typing import TypedDict
from playwright.sync_api import Page
from config.settings import IRMS_BASE_URL
from pages.page import BasePage
from utils.calendar import select_calendar_date_range
from utils.combobox import select_combobox_option
from utils.input import fill_input


class SearchOptions(TypedDict):
    start_date: date
    end_date: date
    module: str
    status_code: str


class ApiLogsPage(BasePage):
    """
    API Logs Page
    """

    DATE_RANGE_TRIGGER_PLACEHOLDER = "Select date range"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page.goto(f"{IRMS_BASE_URL}/en/logs/api-logs")

    def is_heading_visible(self) -> bool:
        return self.page.locator("h1").is_visible()

    def search(self, **kwargs: SearchOptions):
        """
        Searches for API logs by date range, module, and status code.

        Kwargs:
            start_date (date): Start date of the date range
            end_date (date): End date of the date range
            module (str): Module to search for
            status_code (str): Status code to search for
        """
        start_date: date = kwargs.get("start_date")
        end_date: date = kwargs.get("end_date")
        module: str = kwargs.get("module")
        status_code: str = kwargs.get("status_code")

        if start_date and end_date:
            self.select_date_range(start_date=start_date, end_date=end_date)
        if module:
            self.select_module(module=module)
        if status_code:
            self.select_status_code(status_code=status_code)
        self.click_search_button()

    def select_date_range(self, start_date: date, end_date: date):
        select_calendar_date_range(
            page=self.page,
            trigger_placeholder=self.DATE_RANGE_TRIGGER_PLACEHOLDER,
            start_date=start_date,
            end_date=end_date,
        )

    def select_module(self, module: str):
        select_combobox_option(page=self.page, label_text="Module:", value=module)

    def select_status_code(self, status_code: str):
        fill_input(page=self.page, placeholder="Status Code", value=status_code)

    def click_search_button(self):
        self.page.locator("button:has-text('Search')").click()
