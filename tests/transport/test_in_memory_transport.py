import pytest

from src.core.errors import InvalidEventError, InvalidLifecycleError
from src.transport.in_memory.in_memory_transport import InMemoryTransport
from tests.conftest import DummyConsumer


def test_subscribe_adds_consumer(dummy_consumer):
    transport = InMemoryTransport()
    transport.subscribe(dummy_consumer)
    assert dummy_consumer in transport.consumers


def test_unsubscribe_removes_consumer(dummy_consumer):
    transport = InMemoryTransport()
    transport.subscribe(dummy_consumer)
    transport.unsubscribe(dummy_consumer)
    assert dummy_consumer not in transport.consumers


def test_unsubscribe_nonexistent_consumer_raises(dummy_consumer):
    transport = InMemoryTransport()
    with pytest.raises(InvalidLifecycleError):
        transport.unsubscribe(dummy_consumer)


def test_duplicate_subscription_raises(dummy_consumer):
    transport = InMemoryTransport()
    transport.subscribe(dummy_consumer)
    with pytest.raises(InvalidLifecycleError):
        transport.subscribe(dummy_consumer)


def test_publish_invalid_event_raises():
    transport = InMemoryTransport()
    with pytest.raises(InvalidEventError):
        transport.publish("not an event")  # type: ignore


def test_publish_with_consumers(dummy_consumer, dummy_event):
    transport = InMemoryTransport()
    transport.subscribe(dummy_consumer)
    transport.publish(dummy_event)
    transport.flush()
    assert dummy_event in dummy_consumer.received_events


def test_publish_multiple_consumers(dummy_consumer, dummy_event):
    transport = InMemoryTransport()
    another_consumer = DummyConsumer()
    transport.subscribe(dummy_consumer)
    transport.subscribe(another_consumer)
    transport.publish(dummy_event)
    transport.flush()
    assert dummy_event in dummy_consumer.received_events
    assert dummy_event in another_consumer.received_events


def test_publish_without_consumers_raises(dummy_event):
    transport = InMemoryTransport()
    with pytest.raises(InvalidLifecycleError):
        transport.publish(dummy_event)
