
from libs.site_wrapper import SiteWrapper
from playwright.sync_api import Page


class IRMSSiteWrapper(SiteWrapper):
  email: str
  password: str
  page: Page
  is_logged_in: bool

  def __init__(self, **kwargs):
    super().__init__(kwargs.get("url"))
    self.email = kwargs.get("email")
    self.password = kwargs.get("password")

  def login(self):
    self._fill_email()
    self._fill_password()
    self._click_login()
    self._raise_if_error_toast()

  def _raise_if_error_toast(self):
    # Try to find a visible toast/message with 'error' or error indication
    toast = self.page.locator("div:has-text('Invalid username or password')")
    if toast.is_visible():
      error_text = toast.inner_text()
      raise RuntimeError(f"Error toast/message displayed: {error_text}")

  def login(self):
    self._fill_email()
    self._fill_password()
    self._click_login()
    self._raise_if_error_toast()

    
    
    

  def _fill_email(self):
    email_field_input = self.page.locator("input[type='text'][name='email']")
    email_field_input.wait_for(state="visible")
    email_field_input.fill(self.email)

  def _fill_password(self):
    password_field_input = self.page.locator("input[type='password'][name='password']")
    password_field_input.fill(self.password)

  def _click_login(self):
    login_button = self.page.locator("button[type='submit']")
    login_button.click()