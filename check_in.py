"""Daily check in."""
from __init__ import api_check_in_status, session, cookie, login_required, response_post_check


@login_required
@response_post_check
def get_check_in_status():
    """Get check in status."""
    return session.get(api_check_in_status, headers={"cookie": f"sessionid={cookie};"}).json()


@login_required
@response_post_check
def check_in():
    """Check in."""
    return session.post("https://api.juejin.cn/growth_api/v1/check_in",
                        headers={"cookie": f"sessionid={cookie};"},
                        json={}).json()


if __name__ == "__main__" and not get_check_in_status():
    check_in()
