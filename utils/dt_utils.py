__all__ = [
    'utcnow'
]

from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)