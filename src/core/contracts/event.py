from abc import ABC
from dataclasses import dataclass
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

    event_type: str
    step: int
    payload: Dict[str, Any]
