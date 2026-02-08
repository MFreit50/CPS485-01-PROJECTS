from src.core.time.simple_clock import SimpleClock
from src.producers.examples.counter_producer import CounterProducer
from src.producers.examples.fibonacci_producer import FibonacciProducer
from src.producers.examples.random_producer import SeededRandomProducer
from src.consumers.examples.print_consumer import PrintConsumer
from src.transport.in_memory.in_memory_transport import InMemoryTransport
from src.core.trace.simple_runner_tracer import SimpleRunnerTracer
from src.core.execution.simple_runner import SimpleRunner

def main():
    clock = SimpleClock()
    transport = InMemoryTransport()
    consumer = PrintConsumer()
    transport.subscribe(consumer)

    tracer = SimpleRunnerTracer()

    clock = SimpleClock()
    read_only_clock = clock.as_read_only()
    counter_producer = CounterProducer(clock=read_only_clock, limit=5)
    fibonacci_producer = FibonacciProducer(clock=read_only_clock, limit=10)
    random_producer = SeededRandomProducer(clock=read_only_clock, limit=5, seed=42)

    producers = [counter_producer, fibonacci_producer, random_producer]

    runner = SimpleRunner(clock=clock, producers=producers, transport=transport, tracer=tracer)

    print("\n--- Running all producers with tracing ---")
    runner.run()

    print("\n--- Trace Entries ---")
    for entry in tracer.get_trace():
        print(f"[step={entry.step}] producer={entry.producer_id} event={entry.event.event_type} payload={entry.event.payload}")

if __name__ == "__main__":
    main()