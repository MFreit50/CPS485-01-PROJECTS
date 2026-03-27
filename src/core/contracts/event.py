from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Event(ABC):
    """
    Base class for all events emitted by producers

    - Events are immutable
    - Events are serializable
    - Events represent a single meaningful occurrence
    - Contains all relevant data for the consumer to interpret the event

    """

    timestamp: int
    producer_id: str

    @property
    @abstractmethod
    def event_id(self) -> str:
        """
        Unique identifier for the event instance.
        Combines producer ID and timestamp to ensure uniqueness.
        Returns:
            str: The unique event ID
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the event to a dictionary.
        Returns:
            A dictionary representation of the event.
        """
        data = asdict(self)
        data["event_type"] = self.__class__.__name__
        return data
