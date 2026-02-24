import pytest
from playwright.sync_api import sync_playwright
from config.settings import HEADLESS, IRMS_BASE_URL, IRMS_EMAIL, IRMS_PASSWORD


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=HEADLESS,
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()

    # --- Login ---
    page.goto(f"{IRMS_BASE_URL}/en/login")
    page.locator("input[name='email']").wait_for(state="visible", timeout=15_000)
    page.fill("input[name='email']", IRMS_EMAIL)
    page.fill("input[name='password']", IRMS_PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_url("**/dashboard", timeout=15_000)

    yield page

    # --- Logout ---
    page.get_by_role("button", name=IRMS_EMAIL).click()
    page.get_by_role("menuitem", name="Log out").click()

    # --- Close ---
    page.close()
    context.close()
