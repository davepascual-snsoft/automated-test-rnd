from playwright.sync_api import Page

class AddTablePitTest:
  def __init__(self, page: Page):
    self.page = page
    self.page.goto("https://irms-client.platform88.me/en/settings/general/table-pit")
    self.click_add_table_pit_button()

  def click_add_table_pit_button(self):
    add_table_pit_button = self.page.locator("button:has-text('Add Table Pit')").wait_for()
    add_table_pit_button.click()