from datetime import datetime
import pytest
from config.settings import IRMS_BASE_URL
from pages.table_pit_page import TablePitPage
from playwright.sync_api import Page


@pytest.mark.order(2)
def test_edit_table_pit(page: Page):
    """
    Verify a table pit can be edited successfully
    """
    date = datetime.now().strftime("%Y-%m-%dHH:MM:SS")

    description = f"Test Table Pit {date}"
    code = f"TP00{date}"
    zone = "ZN002"
    active = True

    table_pit = TablePitPage(page)
    table_pit.open(IRMS_BASE_URL + "/en/settings/general/table-pit")
    table_pit.click_edit_table_pit_button()
    table_pit.edit_table_pit(
        description=description, code=code, zone=zone, active=active
    )
    page.wait_for_load_state("networkidle")
    assert table_pit.get_title() is not None
    assert table_pit.is_table_pit_edited(description=description, code=code)
