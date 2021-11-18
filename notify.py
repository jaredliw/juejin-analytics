"""Send messages via Telegram bot."""
from os import environ

from __init__ import session, escape_markdown

api_send = "https://api.telegram.org/bot{}/sendMessage"
try:
    telegram_bot_token = environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = environ["TELEGRAM_CHAT_ID"]
except KeyError:
    raise LookupError("TELEGRAM_BOT_TOKEN and/or TELEGRAM_CHAT_ID is not set in the environment variable")


class TelegramError(Exception):
    """TelegramError is raised when the response from Telegram API is not 200 OK."""
    pass


def send_message(message):
    """Send a message via Telegram. Message is written in markdown format."""
    params = {
        "chat_id": telegram_chat_id,
        "parse_mode": "MarkdownV2",  # do not use markdown (version 1)!
        "text": message
    }
    response = session.get(api_send.format(telegram_bot_token), params=params).json()
    if not response['ok']:
        raise TelegramError(f"fail to send message via Telegram ({response['error_code']}): {response['description']}")
    return response


if __name__ == "__main__":
    from time import sleep

    from __init__ import config_filename
    from config_parser import ConfigParser
    from translate import get_pending_recommendations

    data = get_pending_recommendations()

    sent_items = []
    # Record the items that have been sent to prevent repeating messages
    parser = ConfigParser()
    parser.read(config_filename)
    try:
        sent_items = parser["translate"]["sent"]
    except KeyError:
        sent_items = []

    ids = []
    for item in data:
        if str(item["id"]) not in sent_items:
            send_message(f"{escape_markdown(item['recommend_name'])}推荐了一篇文章："
                         f"[{escape_markdown(item['title_src'])}]({item['link_url']})（{item['word_count']} 单词），"
                         f"快去[审核](https://juejin.cn/translate/manage)吧！")
        ids.append(item["id"])
        sleep(1)
    
    parser["translate"] = {"sent": str(ids)}
    parser.write(config_filename)
