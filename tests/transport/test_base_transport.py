import pytest

from src.core.errors import InvalidEventError, InvalidLifecycleError
from src.transport.base.base_transport import BaseTransport
from tests.conftest import DummyConsumer


def test_subscribe_adds_consumer(dummy_consumer):
    transport = BaseTransport()
    transport.subscribe(dummy_consumer)
    assert dummy_consumer in transport.consumers


def test_unsubscribe_removes_consumer(dummy_consumer):
    transport = BaseTransport()
    transport.subscribe(dummy_consumer)
    transport.unsubscribe(dummy_consumer)
    assert dummy_consumer not in transport.consumers


def test_unsubscribe_nonexistent_consumer_raises(dummy_consumer):
    transport = BaseTransport()
    with pytest.raises(InvalidLifecycleError):
        transport.unsubscribe(dummy_consumer)


def test_duplicate_subscription_raises(dummy_consumer):
    transport = BaseTransport()
    transport.subscribe(dummy_consumer)
    with pytest.raises(InvalidLifecycleError):
        transport.subscribe(dummy_consumer)


@pytest.mark.asyncio
async def test_publish_invalid_event_raises():
    transport = BaseTransport()
    await transport.start()
    with pytest.raises(InvalidEventError):
        await transport.publish("not an event")  # type: ignore


@pytest.mark.asyncio
async def test_publish_with_consumers(dummy_consumer, dummy_event):
    transport = BaseTransport()
    transport.subscribe(dummy_consumer)
    await transport.start()
    await transport.publish(dummy_event)
    assert dummy_event in dummy_consumer.received_events


@pytest.mark.asyncio
async def test_publish_multiple_consumers(dummy_consumer, dummy_event):
    transport = BaseTransport()
    await transport.start()
    another_consumer = DummyConsumer()
    transport.subscribe(dummy_consumer)
    transport.subscribe(another_consumer)
    await transport.publish(dummy_event)
    assert dummy_event in dummy_consumer.received_events
    assert dummy_event in another_consumer.received_events


@pytest.mark.asyncio
async def test_publish_without_consumers_raises(dummy_event):
    transport = BaseTransport()
    await transport.start()
    with pytest.raises(InvalidLifecycleError):
        await transport.publish(dummy_event)
