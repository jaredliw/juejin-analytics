"""Daily check in."""
from __init__ import api_check_in_status, session, cookie, login_required, response_post_check, check_in_link, \
    api_check_in_day_count, api_get_total_point, api_lottery_config


@login_required
@response_post_check
def get_check_in_status():
    """Get check in status."""
    return session.get(api_check_in_status, cookies={"sessionid": cookie}).json()


@login_required
@response_post_check
def get_check_in_days():
    """Return the number of day that has checked in."""
    return session.get(api_check_in_day_count, cookies={"sessionid": cookie}).json()


@login_required
@response_post_check
def get_total_points():
    """Get the number of point i.e. KuangShi owned."""
    return session.get(api_get_total_point, cookies={"sessionid": cookie}).json()

    
@login_required
@response_post_check
def check_in():
    """Check in."""
    return session.post(check_in_link, cookies={"sessionid": cookie}, json={}).json()


@login_required
def get_lottery_config():
    """Get lottery config, includes: free lottery count, prizes and point cost."""
    return session.get(api_lottery_config, cookies={"sessionid": cookie}).json()


@login_required
def draw_lottery():
    """Draw a lottery."""
    # todo: possibly signature is required
    return session.get(api_draw_lottery, cookies={"sessionid": cookie}).json()


if __name__ == "__main__":
    from __init__ import escape_markdown
    from notify import send_message

    if not get_check_in_status():
        check_in()

    lottery_config = get_lottery_config()
    for _ in range(lottery_config["free_count"]):
        result = draw_lottery()
        ################################
        # Some info about lottery_type #
        ################################
        # 1: 66 point i.e. KuangShi    #
        # 2: Easter egg -- bug         #
        # 3: Juejin merch              #
        # 4: Big prize!                #
        ################################
        if result["lottery_type"] >= 3:
            send_message(f"恭喜你抽中了一个{escape_markdown(result["lottery_name"])}！")
