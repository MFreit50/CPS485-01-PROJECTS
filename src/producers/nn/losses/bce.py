import math
from typing import List
from src.producers.nn.losses.base import Loss

class BinaryCrossEntropy(Loss):
    EPS = 1e-12 #used to prevent log(0)
    def compute(self, predicted: List[float], expected: List[float]) -> float:
        if len(predicted) != len(expected):
            raise ValueError("Predicted and expected outputs must have same length")
        
        loss: float = 0.0
        for a, y in zip(predicted, expected):
            a = min(max(a, self.EPS), 1.0 - self.EPS)
            loss += -(y * math.log(a) + (1 - y) * math.log(1 - a))

        return loss / len(predicted)
    
    def derivative(self, predicted: List[float], expected: List[float]) -> List[float]:
        if len(predicted) != len(expected):
            raise ValueError("Predicted and expected outputs must have same length")
        
        gradients = []
        for a, y in zip(predicted, expected):
            a = min(max(a, self.EPS), 1.0 - self.EPS)
            gradient = -(y / a) + ((1 - y) / (1 - a))
            gradients.append(gradient / len(predicted))

        return gradients