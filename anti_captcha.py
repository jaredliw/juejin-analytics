from time import time

import cv2

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
    """Identify the gap in slider puzzle."""
    # Read images
    puzzle = cv2.imread(puzzle_filename)
    piece = cv2.imread(piece_filename)

    # Identify edges
    puzzle_edge = cv2.Canny(puzzle, 100, 200)
    piece_edge = cv2.Canny(piece, 100, 200)

    bg_pic = cv2.cvtColor(puzzle_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(piece_edge, cv2.COLOR_GRAY2RGB)

    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    X = max_loc[0]
    th, tw = tp_pic.shape[:2]
    tl = max_loc
    br = (tl[0] + tw, tl[1] + th)
    cv2.rectangle(puzzle, tl, br, (0, 0, 255), 2)
    cv2.imshow('out.jpg', puzzle)
    cv2.waitKey(0)

raw = get_captcha()
download_image(raw["question"]["url1"], "puzzle.jpeg")
download_image(raw["question"]["url2"], "piece.jpeg")
identify_gap_pos("puzzle.jpeg", "piece.jpeg")
