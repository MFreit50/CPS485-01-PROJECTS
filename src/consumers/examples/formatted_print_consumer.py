from pprint import pprint

from src.consumers.base.synchronous_consumer import SynchronousConsumer
from src.core.contracts.event import Event


class FormattedPrintConsumer(SynchronousConsumer):
    """
    Example consumer that prints event details to the console
    in a formatted manner.
    """

    def _handle(self, event: Event) -> None:
        """
        Handles a single event emitted by a producer by printing its details.
        Args:
            event (Event): The event to be handled
        """
        pprint(event.to_dict())
        print()
