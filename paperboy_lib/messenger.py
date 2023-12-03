from paperboy_lib import MessageFormatter


class Messenger:
    def __init__(self):
        pass

    def send(self, message: str):
        raise NotImplementedError

    def sendWithMention(self, message: str):
        raise NotImplementedError

    def resolve_formater(self, formatters: dict[str, MessageFormatter]) -> MessageFormatter:
        return formatters.get("markdown")

