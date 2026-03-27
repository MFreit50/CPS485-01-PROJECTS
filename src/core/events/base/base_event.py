from abc import ABC
from dataclasses import dataclass

from src.core.contracts.event import Event
from src.core.id.identifiable import Identifiable


@dataclass(frozen=True)
class BaseEvent(Event, Identifiable, ABC):
    """
    Base implementation for all events in the system.
    """

    def __post_init__(self):
        Identifiable._initialize_id(self)

    @property
    def event_id(self) -> str:
        """
        Unique identifier for the event instance.
        Combines producer ID and timestamp to ensure uniqueness.
        Returns:
            str: The unique event ID
        """
        return self.id
