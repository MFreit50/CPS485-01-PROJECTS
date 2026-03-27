from dataclasses import dataclass
from typing import Any

from src.core.events.base.base_event import BaseEvent


@dataclass(frozen=True)
class CounterNumber(BaseEvent):
    """
    Emitted when a counter value is incremented by the CounterProducer.
    """

    value: int
