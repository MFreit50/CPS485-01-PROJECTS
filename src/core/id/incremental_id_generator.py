import itertools

from src.core.contracts.id_generator import IDGenerator


class IncrementalIDGenerator(IDGenerator):
    """
    Utility class for generating unique identifiers using UUID4.
    """

    def __init__(self):
        self._counter: itertools.count[int] = itertools.count()

    def generate_id(self) -> int:
        """
        Generate a new integer count id
        Returns:
            int id
        """
        return next(self._counter)
