from typing import TypedDict


class Paper(TypedDict):
    title: str
    abstract: str
    authors: list[str]
    url: str
    submitted_at: str


class Message(TypedDict):
    search_keyword: str
    title: str
    abstract: str
    authors: list[str]
    url: str
    submitted_at: str
