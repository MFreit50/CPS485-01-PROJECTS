import math
from random import random

from src.core.time.simple_clock import SimpleClock
from src.transport.in_memory.in_memory_transport import InMemoryTransport
from src.core.trace.simple_runner_tracer import SimpleRunnerTracer
from src.core.execution.simple_runner import SimpleRunner
from src.producers.base.base_producer import BaseProducer
from src.core.contracts.event import Event
from src.producers.nn.simple_nn import SimpleNeuralNetwork
from src.producers.nn.neuron import Neuron
from src.producers.nn.layer import Layer
from src.consumers.dummy_consumer import DummyConsumer
from src.consumers.examples.print_consumer import PrintConsumer
from src.consumers.examples.formatted_print_consumer import FormattedPrintConsumer
from src.producers.nn.activations.sigmoid import Sigmoid
from src.producers.nn.activations.tanh import Tanh
from src.producers.nn.losses.mse import MeanSquaredError
from src.producers.nn.losses.bce import BinaryCrossEntropy
import random

def main():
    
    sigmoid = Sigmoid()
    tanh = Tanh()
    mse = MeanSquaredError()
    bce = BinaryCrossEntropy()

    #Input layer with 2 inputs and 2 neurons
    input_layer = Layer(neurons=[
        Neuron(rng=random.Random(42), num_inputs=2, activation_function=sigmoid),
        Neuron(rng=random.Random(43), num_inputs=2, activation_function=sigmoid)
        ]
    )

    #Hidden layer with 2 neurons
    hidden_layer = Layer(neurons=[
        Neuron(rng=random.Random(44), num_inputs=2, activation_function=sigmoid),
        Neuron(rng=random.Random(45), num_inputs=2, activation_function=sigmoid)
        ]
    )

    #Hidden layer with 2 neurons
    hidden_layer2 = Layer(neurons=[
        Neuron(rng=random.Random(50), num_inputs=3, activation_function=sigmoid),
        Neuron(rng=random.Random(51), num_inputs=3, activation_function=sigmoid)
        ]
    )

    #Output layer with 1 neuron
    output_layer = Layer(neurons=[
        Neuron(rng=random.Random(46), num_inputs=2, activation_function=sigmoid)
        ]
    )

    #XOR dataset
    inputs = [
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
    ]

    outputs = [
    [0.0],
    [1.0],
    [1.0],
    [0.0]
    ]

    nn_producer = SimpleNeuralNetwork(
        clock=SimpleClock().as_read_only(),
        layers=[input_layer, hidden_layer, output_layer],
        inputs=inputs,
        expected_outputs=outputs,
        loss_function=bce,
        learning_rate=0.01,
        epochs=24000




    )

    transport = InMemoryTransport()
    consumer = FormattedPrintConsumer()
    dummy_consumer = DummyConsumer()
    transport.subscribe(dummy_consumer)
    tracer = SimpleRunnerTracer()

    runner = SimpleRunner(
        clock=SimpleClock(),
        producers=[nn_producer],
        transport=transport,
        tracer=tracer
    )

    print("\n--- Running Simple Neural Network Producer ---")
    runner.run()

    def print_trace_entries():
        print("\n--- Trace Entries ---")
        for entry in tracer.get_trace():
            print(entry)

    def predict():
        for x in inputs:
            y = nn_producer.predict(x)
            print(f"{x} -> {y}")

    #print_trace_entries()
    predict()

if __name__ == "__main__":
    main()