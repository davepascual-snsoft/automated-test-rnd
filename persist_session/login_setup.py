import os
from playwright.sync_api import sync_playwright
from config.settings import (IRMS_BASE_URL, IRMS_EMAIL, IRMS_PASSWORD, HEADLESS)

def save_login_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=HEADLESS)
        context = browser.new_context()
        page = context.new_page()

        # Go to login page
        page.goto(f"{IRMS_BASE_URL}/login")

        # Perform login
        page.fill("input[name='email']", IRMS_EMAIL)
        page.fill("input[name='password']", IRMS_PASSWORD)
        page.click("button[type='submit']")

        # Wait for successful redirect
        page.wait_for_url("**/dashboard")

        # Save session
        storage_path = "persist_session/auth/storage_state.json"
        if not os.path.exists(storage_path):
            os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        context.storage_state(path=storage_path)

        browser.close()

if __name__ == "__main__":
    save_login_state()
