from .watcher import GoogleScholarWatcher
from paperboy_lib.di import register_message_provider


register_message_provider(GoogleScholarWatcher())