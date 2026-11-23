"""A tiny publish/subscribe. Publishers and subscribers share only this module
and the keys of the message."""

from collections import defaultdict
from collections.abc import Callable

Handler = Callable[[dict[str, str]], None]
_subscribers: dict[str, list[Handler]] = defaultdict(list)


def subscribe(event: str, handler: Handler) -> None:
    _subscribers[event].append(handler)


def publish(event: str, data: dict[str, str]) -> None:
    for handler in _subscribers[event]:
        handler(data)
