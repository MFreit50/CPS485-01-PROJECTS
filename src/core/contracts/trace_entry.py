from dataclasses import dataclass
from src.core.contracts.event import Event

@dataclass(frozen=True)
class TraceEntry:
    """
    Immutable record of a single step in algorithm execution.

    Attributes:
        event (Event): The event emitted by the producer
        producer_id (str): The unique identifier of the producer
        step (int): The logical clock time when the event occurred
    """
    event: Event
    producer_id: str
    step: int