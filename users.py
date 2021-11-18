"""Juejin login and user profile."""
from execjs import compile

from __init__ import session, login_required, response_post_check, cookie, api_user, login_link, raise_error
from anti_captcha import anti_captcha


@login_required
@response_post_check
def get_profile():
    """Get the profile of current logged in user."""
    return session.get(api_user, cookies={"sessionid": cookie}).json()


def login(account, password):
    """Login to Juejin account with given credentials."""
    if __name__ != "__main__":
        raise NotImplementedError("under construction")

    with open("login.js", "r") as f:
        text = f.read()
    login_js = compile(text)

    data = {
        "account": login_js.call("encrypt", account),
        "password": login_js.call("encrypt", password),
        "captcha": "",
        "aid": "2608",
        "is_sso": "false",
        "host": "",
        "mix_mode": "1",
    }
    while True:
        response = session.post(login_link, data=data).json()
        if response["message"] == "error":
            if response["data"]["error_code"] == "1105":
                raise_error(response["data"]["error_code"], response["data"]["description"])
            anti_captcha()
        else:
            break
