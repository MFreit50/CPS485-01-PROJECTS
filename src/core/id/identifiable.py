from typing import Hashable

from src.core.contracts.id_generator import IDGenerator
from src.core.id.uuid_generator import UUIDGenerator


class Identifiable:
    """
    A mixin class that provides a unique identifier to any class that inherits from it.
        - Uses an IDGenerator to create unique IDs for each instance
        - Default ID generator is UUIDGenerator, but can be overridden by passing a custom IDGenerator to the constructor
    """

    _default_id_generator: IDGenerator = UUIDGenerator()

    def __init__(
        self, *args, id_generator: IDGenerator | None = None, **kwargs
    ) -> None:
        """
        Initializes the unique identifier for this instance.
        Args:
            id_generator: Optional custom IDGenerator. Defaults to UUIDGenerator.
        """
        super().__init__(*args, **kwargs)
        self._raw_id = (id_generator or self._default_id_generator).generate_id()
        self._id_string = str(self._raw_id)

    def _initialize_id(self, id_generator: IDGenerator | None = None) -> None:
        """
        Initializes the unique identifier for this instance.
        Intended for use by subclasses that cannot invoke __init__ directly,
        such as frozen dataclasses which must perform attribute assignment
        via object.__setattr__ inside __post_init__.
        Raises:
            RuntimeError: If called more than once on the same instance.
        Args:
            id_generator: Optional custom IDGenerator. Defaults to UUIDGenerator.
        """
        if hasattr(self, "_raw_id") or hasattr(self, "_id_string"):
            raise RuntimeError(
                f"_initialize_id called more than once on {self.__class__.__name__}. "
                "ID initialization must only occur once per instance."
            )

        raw_id = (id_generator or self._default_id_generator).generate_id()
        object.__setattr__(self, "_raw_id", raw_id)
        object.__setattr__(self, "_id_string", str(raw_id))

    @property
    def raw_id(self) -> Hashable:
        """
        Returns the unique raw identifier of the instance.
        Returns:
            Hashable: The unique raw identifier
        """
        return self._raw_id

    @property
    def id(self) -> str:
        """
        Returns the unique string identifier of the instance.
        Returns:
            str: The unique string identifier
        """
        return self._id_string

    def __eq__(self, other) -> bool:
        if type(self) is type(other):
            return self.raw_id == other.raw_id
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.raw_id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.id}')"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.id[:8]}...')"
