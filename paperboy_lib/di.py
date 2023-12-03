from paperboy_lib import MessageProvider


__MESSAGE_PROVIDERS = []

def register_message_provider(message_provider: MessageProvider):
    __MESSAGE_PROVIDERS.append(message_provider)
    print(f"registered {message_provider.__class__.__name__}")

def load_message_providers():
    return __MESSAGE_PROVIDERS