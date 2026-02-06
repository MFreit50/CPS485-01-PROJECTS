from src.core.clock.simple_clock import SimpleClock
from src.producers.examples.counter_producer import CounterProducer
from src.producers.examples.fibonacci_producer import FibonacciProducer
from src.producers.examples.random_producer import SeededRandomProducer
from src.consumers.examples.print_consumer import PrintConsumer
from src.transport.in_memory.in_memory_transport import InMemoryTransport

def run_producer(producer, transport) -> None:
    """
    Helper function to run a producer and print its events.
    Args:
        producer: An instance of a Producer to be executed.
    """

    producer.start()

    while not producer.is_finished():
        event = producer.step()
        if event is not None:
            transport.publish(event)

def main():
    clock = SimpleClock()
    consumer = PrintConsumer()
    transport = InMemoryTransport(consumers=[consumer])

    print("\n--- Counter Producer ---")
    counter_producer = CounterProducer(clock=clock, max_value=5)
    run_producer(counter_producer, transport)

    print("\n--- Fibonacci Producer ---")
    fibonacci_producer = FibonacciProducer(clock=clock, max_count=10)
    run_producer(fibonacci_producer, transport)

    print("\n--- Seeded Random Producer ---")
    random_producer = SeededRandomProducer(clock=clock, total_steps=5, seed=42)
    run_producer(random_producer, transport)

if __name__ == "__main__":
    main()