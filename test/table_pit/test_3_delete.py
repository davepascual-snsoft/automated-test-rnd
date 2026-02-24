from playwright.sync_api import Page
import pytest
from pages.table_pit_page import TablePitPage
from config.settings import IRMS_BASE_URL


@pytest.mark.order(3)
def test_delete_table_pit(page: Page):
    """
    Verify a table pit can be deleted successfully
    """

    pit_code = "TP002"

    table_pit = TablePitPage(page)
    table_pit.open(IRMS_BASE_URL + "/en/settings/general/table-pit")
    table_pit.delete_table_pit(code=pit_code)
    page.wait_for_load_state("networkidle")

    assert table_pit.is_table_pit_deleted(code=pit_code)
