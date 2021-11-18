"""All about articles on Juejin."""
from __init__ import session, category_id_map, tag_id_map, api_category_feed, api_recommended_feed, api_tag_feed, \
    response_post_check, api_user_articles

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

        data, has_more, cursor = _response_handler(url, json=json_data)
        if not has_more:
            break

        for record in data:
            yield record[data_container]


def fetch_recommended_articles():
    """Iterator, fetch all data of recommended articles."""
    return _article_list_fetcher(api_recommended_feed, data_container="item_info")


def fetch_articles_by_category(category, tag=None):
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


def fetch_articles_by_user_id(user_id):
    """Get all articles written by the user given."""
    return _article_list_fetcher(api_user_articles, {
        "sort_type": 2,
        "user_id": user_id
    })


# Sync articles to local
if __name__ == "__main__":
    import os
    from re import sub
    from json import loads
    from subprocess import Popen
    from functools import partial
    from unicodedata import normalize

    import execjs
    from bs4 import BeautifulSoup

    from __init__ import config_filename
    from users import get_profile
    from config_parser import ConfigParser

    # Encoding error, execjs' bug
    # Monkey patching
    execjs._external_runtime.Popen = partial(Popen, encoding="utf-8")  # noqa


    def slugify(value, allow_unicode=False):
        """
        Modified from https://github.com/django/django/blob/master/django/utils/text.py.
        Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated dashes to single dashes. Remove
        characters that aren't alphanumerics, underscores, or hyphens. Convert to lowercase. Also strip leading and
        trailing whitespace, dashes, and underscores.
        """
        value = str(value)
        if allow_unicode:
            value = normalize('NFKC', value)
        else:
            value = normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = sub(r'[^\w\s-]', '-', value.lower())
        return sub(r'[-\s]+', '-', value).strip('-_')


    directory = "articles/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    parser = ConfigParser()
    parser.read(config_filename)
    try:
        synced = loads(parser["post"]["article_ids"])
    except KeyError:
        synced = []

    my_articles = ((item["title"], item["article_id"])
                   for item in fetch_articles_by_user_id(get_profile()["user_id"]))
    for article_title, article_id in my_articles:
        if int(article_id) in synced:
            continue

        js_script = BeautifulSoup(session.get(f"https://juejin.cn/post/{article_id}")
                                  .content, "lxml").find_all("script")[-10].string
        compiled_script = execjs.compile("window = global;" + js_script)
        md_content = compiled_script.eval("window.__NUXT__.state.view.column.entry.article_info.mark_content")

        with open(directory + slugify(article_title, allow_unicode=True) + ".md", "w", encoding="utf-8") as file:
            file.write(md_content)

        synced.append(int(article_id))

    parser["post"] = {"article_ids": str(synced)}
    parser.write(config_filename)
