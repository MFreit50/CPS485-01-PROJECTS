from src.consumers.base.synchronous_consumer import SynchronousConsumer
from src.core.contracts.event import Event


class PrintConsumer(SynchronousConsumer):
    """
    Example consumer that prints event details to the console.
    """

    def _handle(self, event: Event) -> None:
        """
        Handles a single event emitted by a producer by printing its details.
        Args:
            event (Event): The event to be handled
        """
        print(event)
