from abc import ABC, abstractmethod
from typing import Any


class IDGenerator(ABC):
    """
    Abstract base class for generating unique identifiers for producers and consumers.

    - Ensures consistent ID generation across the system
    - Can be implemented using various strategies (e.g., UUIDs, incremental counters)
    """

    @abstractmethod
    def generate_id(self) -> Any:
        """
        Generate a unique identifier.
        Returns:
            str: A unique identifier string
        """
        pass
