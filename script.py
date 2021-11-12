"""A handy script that crawls data writes data to JSON file."""
from json import dump
from threading import Thread

from spider import category_id_map, fetch_by_category

all_data = {}
for key in category_id_map.keys():
    all_data.setdefault(key)


def _handler(category, max_retries=5):
    global all_data
    counter = 0
    while True:
        try:
            all_data[category] = list(fetch_by_category(category))
            break
        except BaseException as exc:
            if counter > max_retries:
                raise exc
            counter += 1


class _CustomThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exc = None

    def run(self):
        # exception bubbling
        try:
            super().run()
        except BaseException as exc:  # will be re-raised exception in _CustomThread.join
            self.exc = exc

    def join(self, **kwargs):
        super().join(**kwargs)
        if self.exc:
            try:
                raise RuntimeError("an error occurred in " + self.name)
            except Exception as e:
                raise self.exc from e


thread_pool = []
for key in all_data.keys():
    thread = _CustomThread(target=_handler, args=(key,))  # noqa
    thread.start()
    thread_pool.append(thread)

for thread in thread_pool:
    thread.join()

with open("juejin_articles.json", "w", encoding='utf8') as file:
    dump(all_data, file, ensure_ascii=False)
