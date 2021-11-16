"""Juejin login and user profile."""
from __init__ import session, login_required, response_post_check, api_profile_id, cookie, api_user


@login_required
@response_post_check
def get_profile_id():
    """Get the profile ID of current logged in user."""
    return session.get(api_profile_id, cookies={"sessionid": cookie}).json()


@login_required
@response_post_check
def get_profile(profile_id=None):
    """Get user profile, default to the current logged in user."""
    if profile_id is None:
        profile_id = get_profile_id()["profile_id"]

    return session.get(api_user, cookies={"sessionid": cookie}).json()


if __name__ == "__main__":
    print(get_profile())
