import argparse
from datetime import datetime
from importlib import import_module
import os
import shutil

from paperboy_lib import Messenger, MessageProvider, MessageFormatter
from messengers.discord import DiscordMessenger
from paperboy_lib.di import load_message_providers
from project import ROOT_DIR

requested_extentions = []

messenger: Messenger = DiscordMessenger(
    os.getenv("DISCORD_BOT_TOKEN"),
    os.getenv("DISCORD_CHANNEL_ID"),
    os.getenv("DISCORD_NOTIFIEE")
)
message_providers: list[MessageProvider] = []

post_count = 0


def main():
    init()

    timestamp = datetime.today().strftime("%Y-%m-%d %H:%M")
    send_message(f"[Batch Start🚀] timestamp = {timestamp}")

    for message_provider in message_providers:
        message_provider.sync(on_message_provided)
    notify_result()

    send_message(f"[Batch End🏁] timestamp = {timestamp}")

    exit(0)

def init():
    # This should be called before importing any extentions
    # (configurations files may be refered on init)
    os.environ['PAPERBOY_CONFIG_DIR'] = os.path.join(ROOT_DIR, "config")

    # Create config directory if not exists
    if not os.path.isdir("config"):
        print("config directory not found. creating with samples...")
        shutil.copytree(os.path.join(ROOT_DIR, "config_samples"), os.environ['PAPERBOY_CONFIG_DIR'])

    # Use only feeds extention if extensions are not specified
    if not requested_extentions:
        requested_extentions.append("feeds")
    for extention in requested_extentions:
        import_module(f"extentions.{extention}")

    # Load message providers from extentions
    message_providers.extend(load_message_providers())

def on_message_provided(message, formatters: dict[str, MessageFormatter]):
    formatter = messenger.resolve_formater(formatters)
    send_message(formatter(message))
    increment_count()

def increment_count():
    global post_count
    post_count += 1

def notify_result():
    if post_count > 0:
        send_with_mension(f"New {post_count} paper(s) are found!🎊")
    else:
        send_message(f"No new paper found...😇")

def send_message(message: str):
    messenger.send(message)
    print(message)

def send_with_mension(message: str):
    messenger.sendWithMention(message)
    print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="paperboy")
    parser.add_argument("-e", "--extention", nargs="*", help="specify extention", required=False)
    args = parser.parse_args()

    if args.extention:
        requested_extentions.extend(args.extention)

    main()
