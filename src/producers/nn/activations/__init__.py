from src.producers.nn.activations.registry import ActivationRegistry
from src.producers.nn.activations.relu import ReLU
from src.producers.nn.activations.sigmoid import Sigmoid
from src.producers.nn.activations.tanh import Tanh

ActivationRegistry.register("sigmoid", Sigmoid)
ActivationRegistry.register("tanh", Tanh)
ActivationRegistry.register("relu", ReLU)
