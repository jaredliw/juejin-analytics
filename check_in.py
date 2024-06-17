"""Daily check in."""
from __init__ import api_check_in_status, session, cookie, login_required, response_post_check, check_in_link, \
    api_check_in_day_count, api_get_total_point, api_lottery_config, api_draw_lottery, api_get_luck, \
    api_lottery_history, attract_luck_link


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
@response_post_check
def get_lottery_config():
    """Get lottery config, includes: free lottery count, prizes and point cost."""
    return session.get(api_lottery_config, cookies={"sessionid": cookie}).json()


@response_post_check
def get_lottery_history():
    return session.post(api_lottery_history).json()


@login_required
@response_post_check
def draw_lottery():
    """Draw a lottery."""
    return session.post(api_draw_lottery, cookies={"sessionid": cookie}).json()


@login_required
@response_post_check
def get_luck():
    """Get luck i.e. XingYunZhi. When the value of luck reaches 6000, you will win a Juejin merch!"""
    return session.post(api_get_luck, cookies={"sessionid": cookie}).json()


@login_required
@response_post_check
def attract_luck(lottery_history_id):
    """Attract luck from others who had won a prize. You can do this at most once a day."""
    return session.post(attract_luck_link, cookies={"sessionid": cookie}, json={"lottery_history_id": lottery_history_id}).json()


if __name__ == "__main__":
    from random import choice

    from __init__ import escape_markdown
    from notify import send_message

    if not get_check_in_status():
        check_in()

    lottery_config = get_lottery_config()
    for _ in range(lottery_config["free_count"]):
        result = draw_lottery()
        print(result)
        ################################
        # Some info about lottery_type #
        ################################
        # 1: 66 point i.e. KuangShi    #
        # 2: Easter egg -- bug         #
        # 3: Juejin merch              #
        # 4: Big prize!                #
        ################################
        if result["lottery_type"] >= 3:
            send_message(f"恭喜你抽中了一个{escape_markdown(result['lottery_name'])}！")

    lottery_history = get_lottery_history()["lotteries"]
    # my_luck = attract_luck(choice(lottery_history)["history_id"])["total_value"]
    # if my_luck >= 6000:
    #   send_message(f"你的幸运值（{my_luck}/6000）已满，快去领取实物奖励吧！")
