from typing import List

from src.producers.base.base_producer import BaseProducer
from src.core.contracts.event import Event
from src.producers.nn.layer import Layer
from src.core.events.neural_network.training_complete import TrainingComplete
from src.core.events.neural_network.backward_propagation_step import BackwardPropagationStep
from src.core.events.neural_network.forward_propagation_step import ForwardPropagationStep
from src.core.events.neural_network.loss_computed import LossComputed
from src.core.events.neural_network.weight_update_step import WeightUpdateStep
from src.core.errors import InvalidLifecycleError
from src.producers.nn.nn_state import NN_State as State
from src.producers.nn.losses.base import Loss
from src.producers.nn.models.layer_forward_step_result import LayerForwardStepResult
from src.producers.nn.models.layer_backward_step_result import LayerBackwardStepResult
from src.producers.nn.models.layer_update_step_result import LayerUpdateStepResult

class SimpleNeuralNetwork(BaseProducer):
    #SGD IMPLEMENTATION
    def __init__(
        self,
        clock,
        layers: List[Layer],
        inputs: List[List[float]],
        expected_outputs: List[List[float]],
        loss_function: Loss,
        learning_rate: float = 0.1,
        epochs: int = 10,
    ):
        super().__init__(clock=clock)

        if len(inputs) != len(expected_outputs):
            raise ValueError("Inputs and outputs must have same dataset size")

        self.layers = layers
        self.inputs = inputs
        self.expected_outputs = expected_outputs
        self.learning_rate = learning_rate
        self._epochs = epochs

        self._epoch = 0
        self._sample_index = 0
        self._phase = State.FORWARD_PROPAGATION

        self._layer_index = 0

        self._current_inputs = self.inputs[self._sample_index]
        self._loss_function: Loss = loss_function
        self._total_loss: float = 0.0
        self._grad_inputs: List[float] = []

    def _forward_step(self, timestamp) -> ForwardPropagationStep:
        layer: Layer = self.layers[self._layer_index]

        layer_result: LayerForwardStepResult  = layer.forward_step(self._current_inputs)
        event: ForwardPropagationStep = ForwardPropagationStep.from_forward_result(
                timestamp=timestamp,
                producer_id=self.producer_id,
                epoch=self._epoch,
                sample_index=self._sample_index,
                layer_result=layer_result
        )
        
        self._advance_forward_state()

        return event
    
    def _compute_loss(self, timestamp) -> LossComputed:
        
        expected_output = self.expected_outputs[self._sample_index]
        predicted_output = self._current_inputs
        self._total_loss = self._loss_function.compute(predicted_output, expected_output)
        self._grad_inputs = self._loss_function.derivative(predicted_output, expected_output)

        self._phase = State.BACKWARD_PROPAGATION

        return LossComputed(
            timestamp=timestamp,
            producer_id=self._producer_id,
            epoch=self._epoch,
            sample_index=self._sample_index,
            predicted=predicted_output,
            expected=expected_output,
            loss=self._total_loss,
            grad_inputs=self._grad_inputs.copy()
        )

    def _backward_step(self, timestamp) -> BackwardPropagationStep:
        layer: Layer = self.layers[len(self.layers) - self._layer_index - 1]

        layer_result: LayerBackwardStepResult = layer.backward_step(self._grad_inputs)
        event: BackwardPropagationStep = BackwardPropagationStep.from_backward_result(
            timestamp=timestamp,
            producer_id=self._producer_id,
            epoch=self._epoch,
            sample_index=self._sample_index,
            layer_result=layer_result
        )

        self._advance_backward_state()

        return event

    def _update_step(self, timestamp) -> WeightUpdateStep:
        layer: Layer = self.layers[self._layer_index]

        layer_result: LayerUpdateStepResult = layer.update_step(self.learning_rate)

        event: WeightUpdateStep = WeightUpdateStep.from_update_result(
            timestamp=timestamp,
            producer_id=self._producer_id,
            epoch=self._epoch,
            sample_index=self._sample_index,
            layer_result=layer_result
        )

        self._advance_update_state()

        return event

    def _step(self, timestamp: int) -> Event:
        if self._epoch >= self._epochs:
            self._finished = True
            return TrainingComplete(
                timestamp=timestamp,
                producer_id=self._producer_id,
                final_loss=self._total_loss
            )
        
        match self._phase:
            case State.FORWARD_PROPAGATION:
                return self._forward_step(timestamp)
            case State.COMPUTE_LOSS:
                return self._compute_loss(timestamp)
            case State.BACKWARD_PROPAGATION:
                return self._backward_step(timestamp)
            case State.WEIGHT_UPDATE:
                return self._update_step(timestamp)
            case _:
                raise InvalidLifecycleError("Invalid Neural Network State")

    def _advance_forward_state(self):
        layer = self.layers[self._layer_index]
        if layer.is_complete():
            self._current_inputs = layer.outputs.copy()
            layer.reset()
            self._layer_index += 1

            if self._layer_index >= len(self.layers):
                self._phase = State.COMPUTE_LOSS
                self._layer_index = 0

    def _advance_backward_state(self):
        layer = self.layers[len(self.layers) - self._layer_index - 1]
        if layer.is_complete():
            self._grad_inputs = layer.grad_inputs.copy()
            layer.reset()
            self._layer_index += 1

            if self._layer_index >= len(self.layers):
                self._phase = State.WEIGHT_UPDATE
                self._layer_index = 0

    def _advance_update_state(self):
        layer = self.layers[self._layer_index]
        if layer.is_complete():
            layer.reset()
            self._layer_index += 1

            if self._layer_index >= len(self.layers):
                self._phase = State.FORWARD_PROPAGATION
                self._layer_index = 0
                self._advance_epoch()

    def _advance_epoch(self):
        self._sample_index += 1

        if self._sample_index >= len(self.expected_outputs):
            self._epoch += 1
            self._sample_index = 0
        
        self._zero_grad()
        self._current_inputs = self.inputs[self._sample_index]

    def _zero_grad(self) -> None:
        self._grad_inputs.clear()
        for layer in self.layers:
            layer.zero_grad()

    def predict(self, inputs: List[float]) -> List[float]:
        current_inputs = inputs

        for layer in self.layers:
            outputs: List[float] = []
            for neuron in layer.neurons:
                z = sum(
                    w * x for w, x in zip(neuron.weights, current_inputs)
                ) + neuron.bias
                outputs.append(neuron.activation_function.compute(z))
            current_inputs = outputs

        return current_inputs
