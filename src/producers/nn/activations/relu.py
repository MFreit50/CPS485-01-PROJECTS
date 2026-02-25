import math

from src.producers.nn.activations.base import Activation

class ReLU(Activation):

    def compute(self, z: float) -> float:
        return max(0.0, z)

    def derivative(self, a: float) -> float:
        return 1.0 if a > 0.0 else 0.0