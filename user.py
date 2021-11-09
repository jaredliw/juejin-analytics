"""Login Juejin."""
from execjs import compile

from __init__ import session, login_link, raise_error
from anti_captcha import anti_captcha

with open("login.js", "r") as f:
    text = f.read()
login_js = compile(text)


def encrypt_login_param(param):
    """Encrypt login request's parameter, javascript, code from Juejin."""
    return login_js.call("encrypt", param)


def login(account, password):
    """Login to Juejin account with given credentials."""
    data = {
        "account": encrypt_login_param(account),
        "password": encrypt_login_param(password),
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
                raise_error(response["data"]["error_code"], response["data"]["description"], login_link)
            anti_captcha()
        else:
            break
