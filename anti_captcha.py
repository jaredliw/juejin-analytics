from time import time

import cv2
from execjs import compile

from __init__ import captcha_link, session, raise_error


def get_captcha():
    """Get captcha information from source."""
    data = {
        "lang": "zh",
        "app_name": "juejin_web",
        "h5_sdk_version": "2.23.3",
        "sdk_version": "",
        "iid": "0",
        "did": "0",
        "device_id": "0",
        "ch": "web_text",
        "aid": "2608",
        "os_type": "2",
        "mode": "slide",
        "tmp": str(round(time())),
        "platform": "pc",
        "webdriver": "false",
        "fp": "verify_kuxrwvax_Gk0FiXAg_VRMv_4zEN_8doK_MKWqLp4TZOip",
        "subtype": "slide",
        "challenge_code": "3058",
        "os_name": "windows"
    }
    response = session.get(captcha_link, params=data).json()
    if response["message"] != "验证通过":
        raise_error(data["code"], data["message"], captcha_link)
    return response["data"]


def download_image(url, filename):
    """Download image from url."""
    r = session.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r:
            f.write(chunk)


def identify_gap_pos(puzzle_filename, piece_filename):
    """Identify the gap in slider puzzle, the coordinates or the center of the gap is returned."""
    # Read images
    puzzle = cv2.imread(puzzle_filename)
    piece = cv2.imread(piece_filename)

    # Identify edges
    puzzle_edge = cv2.Canny(puzzle, 100, 200)
    piece_edge = cv2.Canny(piece, 100, 200)

    # Match
    res = cv2.matchTemplate(puzzle_edge, piece_edge, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)  # min_val, max_val, min_loc, max_loc (left-upper corner)

    return max_loc[0] + piece_edge.shape[0] // 2, max_loc[1] + piece_edge.shape[1] // 2


def encrpyt_params(item):
    with open("captcha.js", "r") as f:
        text = f.read()

    js_script = compile(text)
    return js_script.call("encrypt", item)

# raw = get_captcha()
# download_image(raw["question"]["url1"], "puzzle.jpeg")
# download_image(raw["question"]["url2"], "piece.jpeg")
# identify_gap_pos("puzzle.jpeg", "piece.jpeg")
