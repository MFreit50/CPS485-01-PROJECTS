import pytest

from src.transport.in_memory.in_memory_transport import InMemoryTransport
from src.core.contracts.event import Event
from src.core.errors import InvalidLifecycleError
from tests.conftest import dummy_event

def test_subscribe_adds_consumer(dummy_consumer):
    transport = InMemoryTransport()
    transport.subscribe(dummy_consumer)
    assert dummy_consumer in transport.consumers

def test_duplicate_subscription_raises(dummy_consumer):
    transport = InMemoryTransport()
    transport.subscribe(dummy_consumer)
    with pytest.raises(InvalidLifecycleError):
        transport.subscribe(dummy_consumer)

def test_publish_without_consumers_raises():
    transport = InMemoryTransport()

    event = dummy_event()

    with pytest.raises(InvalidLifecycleError):
        transport.publish(event)