from dataclasses import dataclass
from src.core.contracts.event import Event

@dataclass(frozen=True)
class CounterNumber(Event):
    """
    Emitted when a counter value is incremented by the CounterProducer.
    """
    
    value: int