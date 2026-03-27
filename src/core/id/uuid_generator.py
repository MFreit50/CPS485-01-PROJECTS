import uuid

from src.core.contracts.id_generator import IDGenerator


class UUIDGenerator(IDGenerator):
    """
    Utility class for generating unique identifiers using UUID4.
    """

    def generate_id(self) -> uuid.UUID:
        """
        Generate a new UUID4 instance
        Returns:
            A UUID4 instance.
        """

        return uuid.uuid4()
