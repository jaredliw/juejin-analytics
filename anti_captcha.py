"""Bypass Juejin slider CAPTCHA without using Selenium WebDriver."""
from functools import cache
from pprint import pprint
from random import randint
from time import time

import cv2
from execjs import compile

from __init__ import get_captcha_link, session, raise_error, verify_captcha_link


@cache
def load_captcha_js():
    """Load captcha.js and return a execjs context. Cached."""
    with open("captcha.js", "r") as f:
        text = f.read()
    return compile(text)


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
        "tmp": str(round(time() * 1000)),
        "platform": "pc",
        "webdriver": "false",
        "fp": "verify_kuxrwvax_Gk0FiXAg_VRMv_4zEN_8doK_MKWqLp4TZOip",
        "subtype": "slide",
        "challenge_code": "3058",
        "os_name": "windows"
    }
    response = session.get(get_captcha_link, params=data).json()
    if response["message"] != "验证通过":
        raise_error(data["code"], data["message"])
    return response["data"]


def download_image(url, filename):
    """Download image from url."""
    r = session.get(url, stream=True)
    with open(filename, "wb") as img_file:
        for chunk in r:
            img_file.write(chunk)


def identify_gap_pos(puzzle_filename, piece_filename):
    """Identify the gap in slider puzzle, the coordinate of the lower-right corner of the gap and the size of image
    are returned."""
    # Read images
    puzzle = cv2.imread(puzzle_filename)
    piece = cv2.imread(piece_filename)

    # Identify edges
    puzzle_edge = cv2.Canny(puzzle, 100, 200)
    piece_edge = cv2.Canny(piece, 100, 200)

    # Match
    res = cv2.matchTemplate(puzzle_edge, piece_edge, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)  # min_val, max_val, min_loc, max_loc (left-upper corner)

    return max_loc[0] + piece_edge.shape[0], max_loc[1] + piece_edge.shape[1], puzzle.shape[1], puzzle.shape[0]


def encrypt_login_params(params):
    """Encrypt login request's parameter, javascript, code from Juejin."""
    return load_captcha_js().call("encrypt", params)


def forge_mouse_motion(end_x, start_x=randint(60, 65), sample_size=randint(25, 35)):
    """Forge mouse motion while dragging the slider."""
    motion = []
    last_time = 0
    last_x = start_x
    duration = randint(3000, 3500)
    const_y = randint(68, 84)
    avg_time_interval = round(duration / sample_size)

    avg_speed = (end_x - start_x) / duration
    gradient = avg_speed / (-0.5 * duration)
    y_intercept = -(gradient * duration)

    def speed_func(t):
        return gradient * t + y_intercept

    for _ in range(sample_size):
        cur_time = last_time + randint(avg_time_interval - 10, avg_time_interval + 10)
        cur_x = round(last_x + speed_func(cur_time) * (cur_time - last_time))
        motion.append({
            "relative_time": cur_time,
            "x": cur_x,
            "y": const_y
        })
        last_time = cur_time
        last_x = cur_x
    return motion


def anti_captcha():
    """Bypass Juejin slider CAPTCHA."""
    puzzle_filename = "puzzle.jpeg"
    piece_filename = "piece.jpeg"
    scaled_img_width = 340

    response = get_captcha()
    download_image(response["question"]["url1"], puzzle_filename)
    download_image(response["question"]["url2"], piece_filename)
    gap_x, _, width, _ = identify_gap_pos(puzzle_filename, piece_filename)
    print("width", width)
    print("before", gap_x)
    scale = scaled_img_width / width
    gap_x = round(gap_x * scale) - randint(65, 70)
    print("scale", scale)
    print("after", gap_x)
    input("stop here////")
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
        "tmp": str(round(time() * 1000)),
        "platform": "pc",
        "webdriver": "false",
        "fp": "verify_kv3tt03p_9NiSbUjm_QcFz_4r2Y_9DBu_gk30dplYZ0bh",
        "subtype": "slide",
        "challenge_code": response["challenge_code"],
        "os_name": "windows",
        "xx-tt-dd": "qJI7ttpVdGKKbSBvYqmaf0aPo"
    }

    motion = forge_mouse_motion(gap_x)
    pprint(motion)
    data1 = {
        "captchaBody": encrypt_login_params({
            "modified_img_width": scaled_img_width,
            "id": response["id"],
            "mode": "slide",
            "reply": motion
        })
    }
    return session.post(verify_captcha_link, params=data, json=data1).json()
