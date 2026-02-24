from datetime import date
from playwright.sync_api import Page

from pages.api_logs_page import ApiLogsPage


def test_search_api_logs_by_module(page: Page):
    api_logs_page = ApiLogsPage(page)
    api_logs_page.search(
        start_date=date(2026, 2, 16),
        end_date=date(2026, 2, 18),
        module="API Logs",
        status_code="200",
    )

    assert api_logs_page.is_heading_visible()
    assert api_logs_page.page.locator("table tbody tr").count() > 0
