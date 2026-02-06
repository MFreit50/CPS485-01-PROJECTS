from typing import List

from src.core.contracts.event import Event
from src.transport.base.base_transport import BaseTransport

class InMemoryTransport(BaseTransport):
    """
    In-memory transport mechanism for moving events from producers to consumers.

    - Stores events in memory
    - Delivers events to all subscribed consumers immediately upon publishing

    """

    def __init__(self) -> None:
        super().__init__()
        self._events: List[Event] = []

    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribed consumers.
        Args:
            event (Event): The event to be published
        Raises:
            InvalidEventError: if the event is invalid.
        """

        self._events.append(event)

        super().publish(event)

    @property
    def events(self) -> List[Event]:
        """Read-only access to the list of stored events."""
        return self._events.copy()
