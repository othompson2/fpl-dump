import json
import os
import pickle
from typing import TypedDict

from ..constants import HEADERS, URLS
from .squad import Squad

LOGIN_URL = "https://users.premierleague.com/accounts/login/"
LOGOUT_URL = "https://users.premierleague.com/accounts/logout/"
REDIRECT_URL = "https://fantasy.premierleague.com/"

# ------------------------------
# classes
# ------------------------------

class Account(TypedDict):
    id: int
    code: int
    first_name: str
    last_name: str
    email: str
    gender: str
    date_of_birth: str
    region: str

# ------------------------------
# private methods
# ------------------------------

def _format_account(info, profile) -> Account:
    return {
        "id": info["entry"],
        "code": info["id"],
        "profile": profile,
        "first_name": info["first_name"],
        "last_name": info["last_name"],
        "email": info["email"],
        "gender": info["gender"],
        "date_of_birth": info["date_of_birth"],
        "region": info["region"]
    }

def _load_cookies(profile, session):
    filename = f"{profile}.cookies"

    # no cookies stored
    if not os.path.exists(filename):
        return None

    # open and get account
    with open(filename, "rb") as f:
        session.cookies.update(pickle.load(f))
        return session.get(URLS["user"]).json()["player"]


def _save_cookies(profile, session):
    filename = f"{profile}.cookies"
    with open(filename, "wb") as f:
        pickle.dump(session.cookies, f)


def _delete_cookies(profile, session):
    filename = f"{profile}.cookies"
    if os.path.exists(filename):
        os.remove(filename)


# ------------------------------
# public methods
# ------------------------------


def login(self, email, password, profile: str = "default"):
    # check if logged in
    if hasattr(self, "account") and self.account['email'] == email and self.account['profile'] == profile:
        print(f"Already logged in as {email} ({profile})")
        return

    # load account using cookies
    if self.config.cookies:
        account = _load_cookies(profile, self.session)

    # logout if wrong account
    if dict.get(account, "email") != email:
        logout()

    # login in if cookies invalid or wrong account
    if not account:
        headers = {
            "user-agent": HEADERS["user-agent"],
        }
        payload = {
            "login": email,
            "password": password,
            "app": "plfpl-web",
            "redirect_uri": REDIRECT_URL,
        }

        res = self.session.post(LOGIN_URL, data=payload, headers=headers)

        if not res.ok:
            raise ValueError(f"Login failed: {res.reason}")

        _save_cookies(profile, self.session)
        account = self.session.get(URLS["user"]).json()["player"]

    # set account specific info
    self.account = _format_account(account, profile)
    self.squad = Squad(self)
    
    print(f"Logged in as {self.account['email']} ({self.account['profile']})")


def logout(self, clean=False):
    # check if logged in
    if not hasattr(self, "account"):
        print("Not logged in")
        return

    headers = {
        "user-agent": HEADERS["user-agent"],
    }
    payload = {"app": "plfpl-web", "redirect_uri": REDIRECT_URL}

    res = self.session.post(LOGOUT_URL, data=payload, headers=headers)

    if not res.ok:
        raise ValueError(f"Logout failed: {res.reason}")

    self.session.cookies.clear()

    # clear user info
    delattr(self, "account")
    delattr(self, 'squad')

def register(self, email, password, profile: str = "default"):
    pass
