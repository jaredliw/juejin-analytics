from os import environ

from __init__ import session, escape_markdown


api_send = "https://api.telegram.org/bot{}/sendMessage"
try:
    telegram_bot_token = environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = environ["TELEGRAM_CHAT_ID"]
except KeyError:
    raise LookupError("TELEGRAM_BOT_TOKEN and/or TELEGRAM_CHAT_ID is not set in the environment variable")

class TelegramError(Exception):
    pass


def send_message(message):
    data = {
        "chat_id": telegram_chat_id,
        "parse_mode": "Markdown",
        "text": message
    }
    response = session.get(api_send.format(telegram_bot_token), params=data).json()
    if not response['ok']:
        raise TelegramError(f"fail to send message via Teiegram ({response['error_code']}): {response['description']}")
    return response


if __name__ == "__main__":
    from time import sleep

    from translate import get_pending_articles


    data = get_pending_articles()

    sent_items = []
    try:
        with open("sent.txt", "r") as file:
            sent_items = file.read().split("\n")
    except FileNotFoundError:
        pass

    ids = []
    for item in data:
        print(sent_items, item)
        if str(item["id"]) not in sent_items:
            send_message(f"{escape_markdown(item['recommend_name'])}推荐了一篇文章：[{escape_markdown(item['title_src'])}]({item['link_url']})（{item['word_count']} 单词），快去[审核](https://juejin.cn/translate/manage)吧！")
        ids.append(item["id"])
        sleep(1)

    with open("sent.txt", "w") as file:
        for id_ in ids:
            file.write(str(id_) + "\n")
