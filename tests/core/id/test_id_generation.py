from dataclasses import dataclass

from src.consumers.base.base_consumer import BaseConsumer
from src.core.contracts.read_only_clock import ReadOnlyClock
from src.core.events.base.base_event import BaseEvent
from src.core.execution.base.base_runner import BaseRunner
from src.core.time.simple_clock import SimpleClock
from src.producers.base.base_producer import BaseProducer
from src.transport.base.base_transport import BaseTransport


class ConcreteClock(ReadOnlyClock):
    def now(self) -> int:
        return 0


class ConcreteProducer(BaseProducer):
    def __init__(self) -> None:
        super().__init__(clock=ConcreteClock())

    def _step(self, timestamp) -> BaseEvent:
        return BaseEvent(timestamp, "")


class TestBaseProducerId:
    def test_producer_id_returns_string(self):
        assert isinstance(ConcreteProducer().producer_id, str)

    def test_producer_id_is_not_empty(self):
        assert len(ConcreteProducer().producer_id) > 0

    def test_producer_id_matches_identifiable_id(self):
        instance = ConcreteProducer()
        assert instance.producer_id == instance.id

    def test_producer_id_is_unique_per_instance(self):
        assert ConcreteProducer().producer_id != ConcreteProducer().producer_id


class ConcreteConsumer(BaseConsumer):
    async def on_event(self, event):
        pass


class TestBaseConsumerId:
    def test_consumer_id_returns_string(self):
        assert isinstance(ConcreteConsumer().consumer_id, str)

    def test_consumer_id_is_not_empty(self):
        assert len(ConcreteConsumer().consumer_id) > 0

    def test_consumer_id_matches_identifiable_id(self):
        instance = ConcreteConsumer()
        assert instance.consumer_id == instance.id

    def test_consumer_id_is_unique_per_instance(self):
        assert ConcreteConsumer().consumer_id != ConcreteConsumer().consumer_id


@dataclass(frozen=True)
class ConcreteEvent(BaseEvent):
    timestamp: int
    producer_id: str


class TestBaseEventId:
    def test_event_id_returns_string(self):
        assert isinstance(ConcreteEvent(timestamp=0, producer_id="test").event_id, str)

    def test_event_id_is_not_empty(self):
        assert len(ConcreteEvent(timestamp=0, producer_id="test").event_id) > 0

    def test_event_id_matches_identifiable_id(self):
        instance = ConcreteEvent(timestamp=0, producer_id="test")
        assert instance.event_id == instance.id

    def test_event_id_is_unique_per_instance(self):
        a = ConcreteEvent(timestamp=0, producer_id="test")
        b = ConcreteEvent(timestamp=0, producer_id="test")
        assert a.event_id != b.event_id


class ConcreteRunner(BaseRunner):
    def __init__(self) -> None:
        super().__init__(clock=SimpleClock(), transport=BaseTransport())

    def _step(self):
        pass


class TestBaseRunnerId:
    def test_runner_id_returns_string(self):
        assert isinstance(ConcreteRunner().runner_id, str)

    def test_runner_id_is_not_empty(self):
        assert len(ConcreteRunner().runner_id) > 0

    def test_runner_id_matches_identifiable_id(self):
        instance = ConcreteRunner()
        assert instance.runner_id == instance.id

    def test_runner_id_is_unique_per_instance(self):
        assert ConcreteRunner().runner_id != ConcreteRunner().runner_id


class TestBaseTransportId:
    def test_transport_id_returns_string(self):
        assert isinstance(BaseTransport().transport_id, str)

    def test_transport_id_is_not_empty(self):
        assert len(BaseTransport().transport_id) > 0

    def test_transport_id_matches_identifiable_id(self):
        instance = BaseTransport()
        assert instance.transport_id == instance.id

    def test_transport_id_is_unique_per_instance(self):
        assert BaseTransport().transport_id != BaseTransport().transport_id
