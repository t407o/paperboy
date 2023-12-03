import textwrap
from paperboy_lib import MessageFormatter
from .model import Message


class MarkdownFormatter(MessageFormatter):
    def __call__(self, message: Message) -> str:
        message = f"""
            🎺New Arrival🎺 {f'- {message["submitted_at"]}' if message["submitted_at"] else ""}
            **Keyword**: {message['search_keyword']}
            **Title**: {message['title']}
            **Abstract**: {message['abstract']}
            **Author**: {", ".join(message['authors'])}
            **Url**: {blankIfNone(message['url'])}
        """
        return textwrap.dedent(message)[1:-1]

def blankIfNone(value: str):
    return value if value else "(not available)"
