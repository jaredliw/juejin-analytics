"""Data crawling and write data to JSON file."""
from json import dump
from threading import Thread

from spider import category_id_map, fetch_by_category

all_data = {}
for key in category_id_map.keys():
    all_data.setdefault(key)


def _handler(category):
    global all_data
    all_data[category] = list(fetch_by_category(category))


thread_pool = []
for key in all_data.keys():
    thread = Thread(target=_handler, args=(key,))
    thread.start()
    thread_pool.append(thread)

for thread in thread_pool:
    thread.join()

with open("juejin_articles.json", "w", encoding='utf8') as file:
    dump(all_data, file, ensure_ascii=False)
