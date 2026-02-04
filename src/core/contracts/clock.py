from abc import ABC, abstractmethod

class Clock(ABC):
    """
    Abstract base class for all clock implementations

    - Responsible for managing logical time within the system
    
    """

    @abstractmethod
    def tick(self) -> int:
        """
        Advance the clock by one time unit
        Returns:
            The current time after ticking
        """
        pass