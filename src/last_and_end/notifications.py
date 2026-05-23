from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationMessage:
title: str
body: str
severity: str = "info"


def build_notification(title: str, body: str, severity: str = "info") -> NotificationMessage:
return NotificationMessage(title=title.strip(), body=body.strip(), severity=severity)
