import pytest

from src.core.contracts.event import Event
from src.core.contracts.consumer import Consumer
from src.producers.examples.counter_producer import CounterProducer
from src.core.time.simple_clock import SimpleClock


class DummyConsumer(Consumer):
    def __init__(self):
        self.received_events = []
    
    def on_event(self, event: Event) -> None:
        self.received_events.append(event)

class DummyEvent(Event):
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