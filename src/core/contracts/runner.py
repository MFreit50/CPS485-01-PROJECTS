from abc import ABC, abstractmethod

from src.core.contracts.producer import Producer


class Runner(ABC):
    """
    Abstract base class for all execution runners

    - Responsible for orchestrating the execution of producers and consumers
    - Manages the lifecycle of the execution process

    """

    @abstractmethod
    async def start(self) -> None:
        """
        Initialize the execution process

        Raises:
            InvalidLifecycleError: if called more than once
        """
        pass

    @abstractmethod
    async def step(self) -> None:
        """
        Execute a single step of the execution process

        Raises:
            InvalidLifecycleError:
                - if step() is called before start()
                - if step() is called after completion
        """
        pass

    @abstractmethod
    async def run(self) -> None:
        """
        Start the execution process until completion.
        """
        pass

    @abstractmethod
    def add_producer(self, producer: Producer) -> None:
        """
        Add a producer to the execution process.
        Args:
            producer (Producer): The producer to add
        Raises:
            InvalidLifecycleError: if called after start()
        """
        pass

    @abstractmethod
    def is_finished(self) -> bool:
        """
        Check if the execution process has completed.
        Returns:
            True if finished, else False
        """
        pass

    @property
    @abstractmethod
    def runner_id(self) -> str:
        """
        Unique identifier for the runner instance.
        Returns:
            str: The unique runner ID
        """
        pass
