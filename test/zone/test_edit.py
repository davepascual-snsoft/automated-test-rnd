from playwright.sync_api import Page
from config.settings import IRMS_BASE_URL
from pages.zone_page import ZonePage


def test_zone_edit(page: Page):
    """
    Verify a zone can be edited successfully
    """
    zone = ZonePage(page)
    zone.open(IRMS_BASE_URL + "/en/settings/general/zone")
    zone.click_edit_zone_button()
    zone.edit_zone("Test Zone 2", "ZN002", "Cage1", True)
    page.wait_for_load_state("networkidle")
    assert zone.get_title() is not None
    assert zone.is_heading_visible()