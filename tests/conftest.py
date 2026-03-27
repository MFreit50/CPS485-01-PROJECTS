import pytest

from src.consumers.base.synchronous_consumer import SynchronousConsumer
from src.core.contracts.event import Event
from src.core.events.base.base_event import BaseEvent
from src.core.time.simple_clock import SimpleClock
from src.producers.examples.counter_producer import CounterProducer


class DummyConsumer(SynchronousConsumer):
    def __init__(self):
        super().__init__()
        self.received_events = []

    def _handle(self, event: Event) -> None:
        self.received_events.append(event)


class DummyEvent(BaseEvent):
    def __init__(self, timestamp: int, producer_id: str):
        super().__init__(
            timestamp=timestamp,
            producer_id=producer_id,
        )


@pytest.fixture
def dummy_consumer():
    return DummyConsumer()


@pytest.fixture
def counter_producer():
    clock = SimpleClock().as_read_only()
    return CounterProducer(clock=clock, limit=3)


@pytest.fixture
def dummy_event():
    return DummyEvent(timestamp=0, producer_id="test_producer")
