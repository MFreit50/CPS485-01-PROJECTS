from src.core.contracts.event import Event
from src.transport.base.base_transport import BaseTransport

class InMemoryTransport(BaseTransport):
    """
    In-memory transport mechanism for moving events from producers to consumers.
    - Delivers events to all subscribed consumers immediately upon publishing

    """

    def __init__(self) -> None:
        super().__init__()

    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribed consumers.
        Args:
            event (Event): The event to be published
        Raises:
            InvalidEventError: if the event is invalid.
        """

        super().publish(event)
