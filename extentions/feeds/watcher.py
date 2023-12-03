import os
from time import sleep
from datetime import datetime, timedelta
from html2text import HTML2Text
import requests
import feedparser
from paperboy_lib import MessageProvider, OnMessageProvided
from paperboy_lib.io import read_lines, read_str
from .markdown import MarkdownFormatter
from .model import Message
from .openai_client import one_shot


urls = read_lines(os.path.join("feed", "feed_urls.txt"))
prompt_summarize = read_str(os.path.join("feed", "prompt_summarize.txt"))

class FeedsWatcher(MessageProvider):
    def sync(self, on_message_provided: OnMessageProvided):
        for url in urls:
            print(f"fetching {url} ...")
            response = feedparser.parse(url)

            todays_entries = list(filter(is_published_in_last_24_hours(base_time=datetime.now()), response.entries))

            print(f"{len(todays_entries)} new entry(s) found...")
            if len(todays_entries) == 0:
                continue

            for entry in todays_entries:
                message = to_message(entry)
                on_message_provided(message, formatters={ "markdown": MarkdownFormatter() })

                print("sleeping 10 seconds...")
                sleep(10)
            
            print(f"fetching completed: {url}")
    
def is_published_in_last_24_hours(base_time):
    return lambda entry: base_time - datetime(*entry["published_parsed"][:6]) <= timedelta(days=1)

def to_message(entry):
    return Message(
        title = entry["title"],
        abstract = one_shot(get_content(entry["link"]), prompt_summarize),
        url = entry["link"]
    )

def get_content(url):
    h = HTML2Text()
    h.ignore_links = True
    return h.handle(requests.get(url).content.decode())
    