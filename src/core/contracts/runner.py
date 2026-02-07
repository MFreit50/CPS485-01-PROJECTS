from abc import ABC, abstractmethod

class Runner(ABC):
    """
    Abstract base class for all execution runners

    - Responsible for orchestrating the execution of producers and consumers
    - Manages the lifecycle of the execution process

    """

    @abstractmethod
    def start(self) -> None:
        """
        Initialize the execution process

        Raises:
            InvalidLifecycleError: if called more than once
        """
        pass

    @abstractmethod
    def step(self) -> None:
        """
        Execute a single step of the execution process

        Raises:
            InvalidLifecycleError:
                - if step() is called before start()
                - if step() is called after completion
        """
        pass

    @abstractmethod
    def run(self) -> None:
        """
        Start the execution process until completion.
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