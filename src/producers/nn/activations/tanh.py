import math

from src.producers.nn.activations.base import Activation

class Tanh(Activation):

    def compute(self, z: float) -> float:
        return math.tanh(z)

    def derivative(self, a: float) -> float:
        return 1.0 - a * a