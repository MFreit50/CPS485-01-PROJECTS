from src.core.contracts.consumer import Consumer
from src.core.contracts.event import Event

class DummyConsumer(Consumer):
    """
    DummyConusmer
    does nothing when receiving event
    """

    def on_event(self, event: Event) -> None:
        """
        Handles a single event emitted by a producer by printing its details.
        Args:
            event (Event): The event to be handled
        """
        pass