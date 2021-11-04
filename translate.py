from __init__ import api_translate_manage_pending_list, cookie, session, JuejinError, raise_error

def get_pending_articles():
    if cookie is None:
        raise JuejinError("not authenticated")

    data = {
        "page_no": 1,
        "page_size": 20,
        "status": 1,
        "key": ""
    }
    response = session.post(api_translate_manage_pending_list, headers={"Content-Type": "application/json", "cookie": f"sessionid={cookie};"}, json=data).json()
    if response["err_msg"] != "success":
        raise_error(response["err_no"], response["err_msg"], api_translate_manage_pending_list)
    return response["data"]
