import os
from persist_session.login_setup import save_login_state

STORAGE_PATH = "persist_session/auth/storage_state.json"

def ensure_session():
    if not os.path.exists(STORAGE_PATH):
        save_login_state()
