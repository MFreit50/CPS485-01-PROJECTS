from src.core.contracts.consumer import Consumer
from src.core.contracts.event import Event

class PrintConsumer(Consumer):
    """
    Example consumer that prints event details to the console.
    """

    def on_event(self, event: Event) -> None:
        """
        Handles a single event emitted by a producer by printing its details.
        Args:
            event (Event): The event to be handled
        """
        print(event)