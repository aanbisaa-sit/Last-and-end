from typing import Protocol
from .notifications import NotificationMessage

class NotificationAdapter(Protocol):
    def send(self, message: NotificationMessage) -> None:
        ...
