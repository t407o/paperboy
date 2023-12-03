import textwrap
from paperboy_lib import MessageFormatter
from .model import Message


class MarkdownFormatter(MessageFormatter):
    def __call__(self, message: Message) -> str:
        message = f"""
            🎺New Arrival🎺
            **Title**: {message['title']}
            **Abstract**: {message['abstract']}
            **Url**: {message['url']}
        """
        return textwrap.dedent(message)[1:-1]
