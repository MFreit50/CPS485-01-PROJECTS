import pytest

from src.core.time.simple_clock import SimpleClock
from src.core.errors import InvalidLifecycleError
from src.producers.base.base_producer import BaseProducer
from src.core.contracts.event import Event

class DummyProducer(BaseProducer):
    def __init__(self, clock):
        super().__init__(clock=clock)
        self._count = 0

    def _step(self, step: int) -> Event:
        self._count += 1

        event = Event(
            event_type="test",
            step=self.clock.now(),
            payload={"count": self._count}
        )

        if self._count >= 2:
            self._finished = True

        return event

def test_producer_lifecycle():
    clock = SimpleClock()
    producer = DummyProducer(clock)

    with pytest.raises(InvalidLifecycleError):
        producer.step(step=0)

    producer.start()
    event = producer.step(step=0)
    assert event is not None

def test_producer_finishes():
    clock = SimpleClock()
    producer = DummyProducer(clock)
    producer.start()

    producer.step(step=0)
    producer.step(step=1)
    assert producer.is_finished()

    with pytest.raises(InvalidLifecycleError):
        producer.step(step=2)
