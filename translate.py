"""All about Juejin translation project."""
from __init__ import api_translate_manage_pending_list, cookie, session, login_required, response_post_check


@login_required
@response_post_check
def get_pending_recommendations():
    """Get recommended articles under review of admin. Admin privilege needed."""
    data = {
        "page_no": 1,
        "page_size": 20,
        "status": 1,
        "key": ""
    }
    return session.post(api_translate_manage_pending_list, cookies={"sessionid": cookie}, json=data).json()
