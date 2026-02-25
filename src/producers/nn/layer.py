from typing import ClassVar, List

from src.core.errors import InvalidLifecycleError
from src.producers.nn.neuron import Neuron
from src.producers.nn.models.neuron_forward_step_result import NeuronForwardStepResult
from src.producers.nn.models.layer_forward_step_result import LayerForwardStepResult
from src.producers.nn.models.neuron_backward_step_result import NeuronBackwardStepResult
from src.producers.nn.models.layer_backward_step_result import LayerBackwardStepResult
from src.producers.nn.models.neuron_update_step_result import NeuronUpdateStepResult
from src.producers.nn.models.layer_update_step_result import LayerUpdateStepResult


class Layer:

    _counter: ClassVar[int] = 0

    def __init__(self, neurons: List[Neuron]):
        if not neurons:
            raise ValueError("Layer must contain at least one neuron")

        self.id = f"{self.__class__.__name__}_{Layer._counter}"
        Layer._counter += 1

        self.neurons = neurons

        self._is_complete = False
        self._neuron_index: int = 0
        self.outputs: List[float] = []
        self.grad_inputs: List[float] = []

    def forward_step(self, inputs: List[float]) -> LayerForwardStepResult:
        if self.is_complete():
            raise InvalidLifecycleError("Layer iteration has already been completed")
            
        neuron = self.neurons[self._neuron_index]
        self._neuron_index += 1

        result: NeuronForwardStepResult = neuron.forward(inputs)
        self.outputs.append(result.activation)

        if self._neuron_index >= len(self.neurons):
            self._is_complete = True
        
        return LayerForwardStepResult(
            layer_id = self.id,
            neuron_result = result
        )
    
    def backward_step(self, grad_inputs: List[float]) -> LayerBackwardStepResult:
        if self.is_complete():
            raise InvalidLifecycleError("Layer iteration has already been completed")
        if len(grad_inputs) != len(self.neurons):
            raise ValueError(f"Layer {self.id} expected {len(self.neurons)} grad_inputs but got {len(grad_inputs)}")
            
        neuron = self.neurons[len(self.neurons) - self._neuron_index - 1]
        gradient: float = grad_inputs[len(grad_inputs) - self._neuron_index - 1]
        self._neuron_index += 1

        result: NeuronBackwardStepResult = neuron.backward(gradient)
        
        if not self.grad_inputs:
            self.grad_inputs = [0.0] * len(result.grad_inputs)
        for i, dx in enumerate(result.grad_inputs):
            self.grad_inputs[i] += dx

        if self._neuron_index >= len(self.neurons):
            self._is_complete = True

        return LayerBackwardStepResult(
            layer_id = self.id,
            neuron_result = result
        )
    
    def update_step(self, learning_rate: float) -> LayerUpdateStepResult:
        if self.is_complete():
            raise InvalidLifecycleError("Layer iteration has already been completed")
        
        neuron = self.neurons[self._neuron_index]
        self._neuron_index += 1

        result: NeuronUpdateStepResult = neuron.update(learning_rate)
        if self._neuron_index >= len(self.neurons):
            self._is_complete = True

        return LayerUpdateStepResult(
            layer_id=self.id,
            neuron_result=result
        )

    def zero_grad(self) -> None:
        self.outputs.clear()
        self.grad_inputs.clear()
        for neuron in self.neurons:
            neuron.zero_grad()

    def is_complete(self):
        return self._is_complete
    
    def reset(self):
        self.outputs.clear()
        self.grad_inputs.clear()
        self._neuron_index = 0
        self._is_complete = False