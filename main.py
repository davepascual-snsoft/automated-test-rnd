from irms.main import IRMSSiteWrapper
from irms.test.add_table_pit import AddTablePitTest
from persist_session.login_setup import save_login_state


def main():

  # EMAIL = "dave@example.com"
  # PASSWORD = "admin123"

  # site = IRMSSiteWrapper(url="https://irms-client.platform88.me/en/login", email=EMAIL, password=PASSWORD)
  # site.login()

  # add_table_pit_test = AddTablePitTest(site.get_page())

  # print("Automation test RND")
  # input("Press Enter to exit (browser will stay open until then)...")
  save_login_state()

if __name__ == "__main__":
  main()