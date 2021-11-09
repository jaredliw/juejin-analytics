"""Call Juejin API and handle requests."""
from __init__ import session, category_id_map, tag_id_map, api_category_feed, api_recommended_feed, api_tag_feed, \
    response_post_check

max_retries = 5


@response_post_check(return_keys=("data", "has_more", "cursor"))
def _response_handler(*args, **kwargs):
    retry_count = 0
    while True:
        try:
            return session.post(*args, **kwargs).json()
        except Exception as e:
            retry_count += 1
            if retry_count > max_retries:
                raise e


def _article_list_fetcher(url, additional_json=None, data_container="article_info"):
    cursor = "0"
    while True:
        json_data = {"cursor": cursor}
        if additional_json is not None:
            json_data.update(additional_json)

        data = _response_handler(url, json=json_data)
        if not data["has_more"]:
            break

        cursor = data["cursor"]
        for record in data["data"]:
            yield record[data_container]


def fetch_recommended():
    """Iterator, fetch all data of recommended articles."""
    return _article_list_fetcher(api_recommended_feed, data_container="item_info")


def fetch_by_category(category, tag=None):
    """Iterator, fetch all data of articles in the given category, filtered by tag (optional)."""
    error_str = "value for parameter '{}' should be one of the following: {}, not '{}'"
    if category not in category_id_map:
        raise ValueError(error_str.format("category", category_id_map.keys(), category))
    if category is not None and category not in category_id_map:
        raise ValueError(error_str.format("tag", list(tag_id_map[category].keys()) + [None], tag))
    
    if tag is None:
        return _article_list_fetcher(api_category_feed, {
            "cate_id": category_id_map[category]
        })
    else:
        return _article_list_fetcher(api_tag_feed, {
            "cate_id": category_id_map[category],
            "tag_id": tag_id_map[category][tag]
        })
