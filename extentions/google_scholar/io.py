import os

from .model import Paper


def save_search_history_to(file: str, paper: Paper):
    with open(os.path.join(os.environ.get("PAPERBOY_CONFIG_DIR"), "google_scholar", file), "a+", encoding="utf-8") as f:
        f.write(f"{paper['title']}\n")
