from abc import ABC
from dataclasses import dataclass

from src.core.contracts.event import Event
from src.core.id.identifiable import Identifiable
from src.core.id.incremental_id_generator import IncrementalIDGenerator


@dataclass(frozen=True)
class FastEvent(Event, Identifiable, ABC):
    """
    Base implementation designed for events that are emitted
    rapidly and ephemerally. While regular events use UUID for identity
    FastEvent uses a simple integer count to reduce cpu and memory consumption
    from in memory persistance
    """

    def __post_init__(self):
        Identifiable._initialize_id(self, IncrementalIDGenerator())

    @property
    def event_id(self) -> str:
        """
        Unique identifier for the event instance.
        Combines producer ID and timestamp to ensure uniqueness.
        Returns:
            str: The unique event ID
        """
        return self.id
