import os
import re
from time import sleep
from typing import Tuple

from scholarly import scholarly
from paperboy_lib import MessageProvider, OnMessageProvided
from paperboy_lib.io import read_lines, read_str
from .openai_client import one_shot
from .io import save_search_history_to
from .markdown import MarkdownFormatter
from .model import Paper

SEARCH_LIMIT = int(os.environ.get("SEARCH_LIMIT") or 10)
BATCH_SIZE = int(os.environ.get("BATCH_SIZE") or 10)

search_keywords = []
post_histories = set()

# list of (keyword, paper)
summarize_queue: list[Tuple[str, Paper]] = []

class GoogleScholarWatcher(MessageProvider):
    def sync(self, on_message_provided: OnMessageProvided):
        
        global post_histories, search_keywords
        search_keywords = read_lines(os.path.join("google_scholar", "search_keywords.txt"))
        post_histories = set(read_lines(os.path.join("google_scholar", "search_histories.txt")))
        prompt_summarize = read_str(os.path.join("google_scholar", "prompt_summarize.txt"))

        if not search_keywords:
            print("No search keywords found! Check the search_keywords.txt")
            exit(1)

        for keyword in search_keywords:
            papers = self.search(keyword, SEARCH_LIMIT)

            new_papers = list(filter(is_new_paper, papers))

            print(f"new papers - {len(new_papers)} hits")
            print(f"returns {BATCH_SIZE} papers of {len(new_papers)} new papers")

            enqueue_all(keyword, new_papers[:BATCH_SIZE])

            print("waiting for 10 seconds... (to avoid rate limit)")
            sleep(10)
        
        while summarize_queue:
            keyword, paper = dequeue()

            paper["abstract"] = one_shot(paper["abstract"], prompt_summarize)

            on_message_provided({ "search_keyword": keyword, **paper }, formatters={ "markdown": MarkdownFormatter() })
            append_to_post_histories(paper)

            sleep(10)

    def search(self, keyword, limit) -> list[Paper]:
        search_results = scholarly.search_pubs(keyword, sort_by="date")

        sliced_results = []
        for _ in range(limit):
            try:
                sliced_results.append(self.format(next(search_results)))
            except StopIteration:
                break

        return sliced_results

    def format(self, search_result) -> Paper:
        abstract = search_result["bib"]["abstract"]
        submitted_at = re.search(r"\d+ days ago - ", abstract)

        if submitted_at:
            abstract = abstract[len(submitted_at.group()) :]
            submitted_at = submitted_at.group().replace(" - ", "")

        return Paper(
            title=search_result["bib"]["title"],
            abstract=abstract,
            authors=search_result["bib"]["author"],
            url=search_result.get("pub_url"),
            submitted_at=submitted_at,
        )

def enqueue_all(keyword: str, papers: list[Paper]):
    for i, paper in enumerate(papers):
        print(f"{i+1}. {paper["title"]}")
        summarize_queue.append((keyword, paper))

def dequeue() -> Tuple[str, Paper]:
    return summarize_queue.pop(0)

def is_new_paper(paper: Paper):
    return paper["title"] not in post_histories

def append_to_post_histories(paper: Paper):
    print(f"recording search history... title={paper["title"]}")
    post_histories.add(paper["title"])
    save_search_history_to("search_histories.txt", paper)
