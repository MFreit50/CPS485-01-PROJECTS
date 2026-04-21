import random

from src.consumers.dummy_consumer import DummyConsumer
from src.consumers.examples.formatted_print_consumer import FormattedPrintConsumer
from src.core.execution.simple_runner import SimpleRunner
from src.core.time.simple_clock import SimpleClock
from src.core.trace.simple_runner_tracer import SimpleRunnerTracer
from src.producers.nn.builder.simple_nn_builder import SimpleNNBuilder
from src.transport.in_memory.in_memory_transport import InMemoryTransport


def main():
    # XOR dataset
    inputs = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    outputs = [[0.0], [1.0], [1.0], [0.0]]

    nn_builder = SimpleNNBuilder(clock=SimpleClock().as_read_only())
    nn = (
        nn_builder.input_dataset(inputs.copy(), outputs)
        .add_layer(2, "sigmoid")
        .add_layer(2, "sigmoid")
        .add_layer(1, "sigmoid")
        .loss("bce")
        .learning_rate(1.5)
        .epochs(3000)
        .rng(random.Random(42))
        .build()
    )

    transport = InMemoryTransport()
    dummy_consumer = DummyConsumer()
    consumer = FormattedPrintConsumer()
    transport.subscribe(dummy_consumer)
    # transport.subscribe(consumer)
    tracer = SimpleRunnerTracer()

    runner = SimpleRunner(
        clock=SimpleClock(), producers=[nn], transport=transport, tracer=tracer
    )

    print("\n--- Running Simple Neural Network Producer ---")
    runner.run()

    def predict():
        for x in inputs:
            y = nn.predict(x)
            print(f"{x} -> {y}")

    predict()


if __name__ == "__main__":
    main()
