from pages.zone_page import ZonePage
from config.settings import IRMS_BASE_URL
from playwright.sync_api import Page


def test_zone_create(page: Page):
    """
    Verify a new zone can be created successfully
    """
    description = "Test Zone 2"
    code = "ZN002"
    cage = "Cage1"

    zone = ZonePage(page)
    zone.open(IRMS_BASE_URL + "/en/settings/general/zone")
    zone.click_add_zone_button()
    zone.create_zone(description, code, cage, True)

    page.wait_for_load_state("networkidle")

    assert zone.get_title() is not None
    assert zone.is_heading_visible()
    assert zone.is_zone_created(description)
