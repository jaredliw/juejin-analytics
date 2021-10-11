from bidict import bidict
from pprint import pprint as print
from requests import Session


class JueJinConnectionError(Exception):
    pass


def _post_request_handler(*args, **kwargs):
    data = session.post(*args, **kwargs).json()
    if data["err_msg"] != "success":
        raise JueJinConnectionError(f"error {data['err_no']} ({data['err_msg']}) while fetching data from '{api_recommend}'")
    return data


def _article_list_fetcher(url, additional_json=None, data_container="article_info"):   
    cursor = "0"
    while True:
        json_data = {"cursor": cursor}
        if additional_json is not None:
            json_data.update(additional_json)
        data = _post_request_handler(url, json=json_data)
        if not data["has_more"]:
            break
        cursor = data["cursor"]
        for record in data["data"]:
            yield record[data_container]
    
    
session = Session()
api_tag_list = "https://api.juejin.cn/recommend_api/v1/tag/recommend_tag_list"
api_recommended_feed = "https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed"
api_category_feed = "https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed"
api_tag_feed = "https://api.juejin.cn/recommend_api/v1/article/recommend_cate_tag_feed"
category_id_map = bidict({
    "后端": "6809637769959178254",
    "前端": "6809637767543259144",
    "Android": "6809635626879549454",
    "iOS": "6809635626661445640",
    "人工智能": "6809637773935378440",
    "开发工具": "6809637771511070734",
    "代码人生": "6809637776263217160",
    "阅读": "6809637772874219534",
})
tag_id_map = {
    "后端": bidict(),
    "前端": bidict(),
    "Android": bidict(),
    "iOS": bidict(),
    "人工智能": bidict(),
    "开发工具": bidict(),
    "代码人生": bidict(),
    "阅读": bidict()
}
for cat_name, cat_id in category_id_map.items():
    tags = _post_request_handler(api_tag_list, json={"cate_id": cat_id})["data"]
    for tag in tags:
        tag_id_map[cat_name][tag["tag_name"]] = tag["tag_id"]


def fetch_recommended():
    """Fetch all data of recommended articles."""
    return _article_list_fetcher(api_recommended_feed, data_container="item_info")


def fetch_by_category(category, tag=None):
    error_str = "value for parameter '{}' should be one of the following: {}, not '{}'"
    if category not in category_id_map:
        raise ValueError(error_str.format("category", category_id_map.keys(), category))
    if category is not None and category not in category_id_map:
        raise ValueError(error_str.format("tag", tag_id_map[category].keys() + [None], tag))
    
    if tag is None:
        return _article_list_fetcher(api_category_feed, {"cate_id": category_id_map[category]})
    else:
        return _article_list_fetcher(api_tag_feed, {"cate_id": category_id_map[category], "tag_id": tag_id_map[category][tag]})
