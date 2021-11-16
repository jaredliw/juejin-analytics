"""Daily check in."""
from __init__ import api_check_in_status, session, cookie, login_required, response_post_check, check_in_link


@login_required
@response_post_check
def get_check_in_status():
    """Get check in status."""
    return session.get(api_check_in_status, cookies={"sessionid": cookie}).json()


@login_required
@response_post_check
def check_in():
    """Check in."""
    return session.post(check_in_link, cookies={"sessionid": cookie}, json={}).json()

print(check_in())
if __name__ == "__main__" and not get_check_in_status():
    check_in()
