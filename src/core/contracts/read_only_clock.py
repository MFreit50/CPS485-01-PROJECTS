from abc import ABC, abstractmethod

class ReadOnlyClock(ABC):
    """
    Abstract base class for read-only clock implementations

    - Provides a way to access the current time without allowing modifications to ensure determinism

    """

    @abstractmethod
    def now(self) -> int:
        """
        Get the current time without advancing the clock
        Returns:
            The current time
        """
        pass