from abc import ABC, abstractmethod
from typing import List

class Loss(ABC):
    """
    Base Class for loss functions
    """
    
    @abstractmethod
    def compute(self, predicted: List[float], expected: List[float]) -> float:
        pass

    @abstractmethod
    def derivative(self, predicted: List[float], expected: List[float]) -> List[float]:
        pass