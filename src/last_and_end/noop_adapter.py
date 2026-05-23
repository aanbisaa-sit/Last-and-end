from .notifications import NotificationMessage


class NoopNotificationAdapter:
def __init__(self) -> None:
    self.messages: list[NotificationMessage] = []

def send(self, message: NotificationMessage) -> None:
    self.messages.append(message)
