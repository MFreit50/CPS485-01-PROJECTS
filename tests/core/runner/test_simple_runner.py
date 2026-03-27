import pytest

from src.core.execution.simple_runner import SimpleRunner
from src.core.time.simple_clock import SimpleClock
from src.core.trace.simple_runner_tracer import SimpleRunnerTracer
from src.transport.in_memory.in_memory_transport import InMemoryTransport


@pytest.mark.asyncio
async def test_runner_records_trace(counter_producer, dummy_consumer):
    clock = SimpleClock()
    transport = InMemoryTransport()
    tracer = SimpleRunnerTracer()
    transport.subscribe(dummy_consumer)

    runner = SimpleRunner(clock=clock, transport=transport, tracer=tracer)
    runner.add_producer(counter_producer)

    await runner.run()

    trace = tracer.get_trace()
    assert len(trace) > 0
    assert trace[0].producer_id == counter_producer.producer_id
