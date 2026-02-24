from playwright.sync_api import Page, sync_playwright

class SiteWrapper:

  url: str
  page: Page

  def __init__(self, url: str):
    self.url = url
    self._playwright = sync_playwright().start()
    browser = self._playwright.chromium.launch(headless=False)
    print(browser)
    self.page = browser.new_page()
    self.page.goto(self.url)

  def get_page(self):
    return self.page

  def close(self):
    self.page.close()
    self._playwright.stop()