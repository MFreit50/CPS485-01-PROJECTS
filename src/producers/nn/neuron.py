from typing import ClassVar, Callable, List
import random

from src.producers.nn.activations.base import Activation
from src.producers.nn.models.neuron_forward_step_result import NeuronForwardStepResult
from src.producers.nn.models.neuron_backward_step_result import NeuronBackwardStepResult
from src.producers.nn.models.neuron_update_step_result import NeuronUpdateStepResult

class Neuron:

    _counter: ClassVar[int] = 0

    def __init__(
        self,
        num_inputs: int,
        activation_function: Activation,
        rng: random.Random | None = None
    ):
        self.id = f"{self.__class__.__name__}_{Neuron._counter}"
        Neuron._counter += 1

        self.activation_function: Activation = activation_function
        rng = rng or random.Random()
        self.weights: List[float] = [rng.uniform(-0.5, 0.5) for _ in range(num_inputs)]
        self.bias: float = rng.uniform(-0.5, 0.5)

        #Cache for backpropagation
        self.last_inputs: List[float] = []
        self.last_z: float = 0.0    #z = Wx + b
        self.last_a: float = 0.0    #a = activation(z)
        self.delta: float = 0.0

        #Cache for optimizer
        self.grad_weights: List[float] = []
        self.grad_bias: float = 0.0

    def forward(self, inputs: List[float]) -> NeuronForwardStepResult:
        if len(inputs) != len (self.weights):
            raise ValueError(f"Neuron {self.id} expected {len(self.weights)} inputs but got {len(inputs)}")
        
        weighted_sum: float  = 0.0
        for W, x in zip(self.weights, inputs):
            weighted_sum += W * x

        z = weighted_sum + self.bias
        a = self.activation_function.compute(z)

        self.last_inputs = inputs.copy()
        self.last_z = z
        self.last_a = a

        return NeuronForwardStepResult(
            neuron_id=self.id,
            inputs=self.last_inputs.copy(),
            weights=self.weights.copy(),
            bias=self.bias,
            z=z,
            activation=a
        )

    def backward(self, gradient: float) -> NeuronBackwardStepResult:
        if len(self.last_inputs) != len (self.weights):
            raise ValueError(f"Neuron {self.id} expected {len(self.weights)} inputs but got {len(self.last_inputs)}")
        
        dz = self.activation_function.derivative(self.last_a)
        self.delta = gradient * dz
        dW = [self.delta * x for x in self.last_inputs]
        dx = [self.delta * W for W in self.weights]
        db = self.delta

        self.grad_weights = dW.copy()
        self.grad_bias = db

        return NeuronBackwardStepResult(
            neuron_id=self.id,
            grad_output=gradient,
            delta=self.delta,
            grad_z=dz,
            grad_weights=dW,
            grad_inputs=dx,
            grad_bias=db
        )
    
    def update(self, learning_rate: float) -> NeuronUpdateStepResult:
        for i, dW in enumerate(self.grad_weights):
            self.weights[i] -= dW * learning_rate
        
        self.bias -= self.grad_bias * learning_rate

        return NeuronUpdateStepResult(
            neuron_id=self.id,
            updated_weights=self.weights.copy(),
            updated_bias=self.bias
        )

    def zero_grad(self) -> None:
        self.last_inputs.clear()
        self.grad_weights.clear()


