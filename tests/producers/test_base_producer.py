import pytest
from src.core.time.simple_clock import SimpleClock
from src.core.errors import InvalidLifecycleError
from src.producers.base.base_producer import BaseProducer
from src.core.contracts.event import Event

class DummyProducer(BaseProducer):
    def __init__(self, clock):
        super().__init__(clock=clock)
        self._count = 0

    def _step(self):
        self._count += 1

        if self._count > 2:
            self._finished = True
            return None

        return Event(
            event_type="test",
            step=self.clock.now(),
            payload={"count": self._count}
        )

def test_producer_lifecycle():
    clock = SimpleClock()
    producer = DummyProducer(clock)

    with pytest.raises(InvalidLifecycleError):
        producer.step()

    producer.start()
    event = producer.step()
    assert event is not None

def test_producer_finishes():
    clock = SimpleClock()
    producer = DummyProducer(clock)
    producer.start()

    producer.step()
    producer.step()
    producer.step()

    assert producer.is_finished()