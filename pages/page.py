from playwright.sync_api import Page

class BasePage:
  def __init__(self, page: Page):
        self.page = page

  def open(self, base_url: str):
      self.page.goto(base_url)

  def get_title(self) -> str:
      return self.page.title()

  def is_heading_visible(self) -> bool:
      return self.page.locator("h1").is_visible()