from __future__ import annotations

import random
from typing import List, Optional, Type

from src.core.contracts.read_only_clock import ReadOnlyClock
from src.producers.nn.activations.base import Activation
from src.producers.nn.activations.registry import ActivationRegistry
from src.producers.nn.layer import Layer
from src.producers.nn.losses.base import Loss
from src.producers.nn.losses.registry import LossRegistry
from src.producers.nn.neuron import Neuron
from src.producers.nn.simple_nn import SimpleNeuralNetwork


class SimpleNNBuilder:

    def __init__(self, clock: ReadOnlyClock):
        self._clock = clock
        self._layers_config: List[tuple[int, Activation]] = []
        self._inputs: Optional[List[List[float]]] = None
        self._outputs: Optional[List[List[float]]] = None
        self._loss: Optional[Loss] = None
        self._learning_rate: float = 0.1
        self._epochs: int = 10
        self._rng = random.Random()

    def input_dataset(
        self, inputs: List[List[float]], outputs: List[List[float]]
    ) -> SimpleNNBuilder:
        if len(inputs) != len(outputs):
            raise ValueError("Inputs and outputs must have same dataset size")

        self._inputs = inputs
        self._outputs = outputs
        return self

    def loss(self, loss: str | Type[Loss]) -> SimpleNNBuilder:
        if isinstance(loss, str):
            loss_cls = LossRegistry.get(loss)
            self._loss = loss_cls()
        elif issubclass(loss, Loss):
            self._loss = loss()
        else:
            raise ValueError("Loss must be a string or a Loss subclass")

        return self

    def learning_rate(self, lr: float) -> SimpleNNBuilder:
        self._learning_rate = lr
        return self

    def epochs(self, epochs: int) -> SimpleNNBuilder:
        self._epochs = epochs
        return self

    def rng(self, rng: random.Random) -> SimpleNNBuilder:
        self._rng = rng
        return self

    def add_layer(
        self, num_neurons: int, activation: str | Type[Activation]
    ) -> SimpleNNBuilder:
        if isinstance(activation, str):
            activation_cls = ActivationRegistry.get(activation)
            activation_instance = activation_cls()
        elif issubclass(activation, Activation):
            activation_instance = activation()
        else:
            raise ValueError("Activation must be a string or an Activation subclass")

        self._layers_config.append((num_neurons, activation_instance))
        return self

    def _build_layers(self) -> List[Layer]:
        if self._inputs is None:
            raise ValueError("Dataset must be provided before building layers")

        layers: List[Layer] = []
        input_size = len(self._inputs[0])

        for num_neurons, activation_function in self._layers_config:
            neurons = [
                Neuron(num_inputs=input_size, rng=self._rng) for _ in range(num_neurons)
            ]

            layer = Layer(neurons, activation_function=activation_function)
            layers.append(layer)

            input_size = num_neurons

        return layers

    def build(self) -> SimpleNeuralNetwork:
        if self._inputs is None or self._outputs is None:
            raise ValueError("Dataset must be set")

        if self._loss is None:
            raise ValueError("Loss function must be set")

        if not self._layers_config:
            raise ValueError("At least one layer must be added")

        layers = self._build_layers()

        return SimpleNeuralNetwork(
            clock=self._clock,
            layers=layers,
            inputs=self._inputs,
            expected_outputs=self._outputs,
            loss_function=self._loss,
            learning_rate=self._learning_rate,
            epochs=self._epochs,
        )
