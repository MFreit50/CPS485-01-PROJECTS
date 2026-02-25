import math

from src.producers.nn.activations.base import Activation

class Sigmoid(Activation):

    def compute(self, z: float) -> float:
        return 1 / (1 + math.exp(-z))

    def derivative(self, a: float) -> float:
        return a * (1 - a)