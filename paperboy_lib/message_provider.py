from typing import Protocol


class MessageFormatter(Protocol):
    def __call__(self, message: dict) -> str:
        raise NotImplementedError

class OnMessageProvided(Protocol):
    def __call__(self, message: dict, formatters: dict[str, MessageFormatter]) -> None:
        raise NotImplementedError

class MessageProvider:
    def sync(self, on_message_provided: OnMessageProvided):    
        raise NotImplementedError
