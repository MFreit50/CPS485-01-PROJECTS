from unittest.mock import MagicMock

from src.core.contracts.id_generator import IDGenerator


def make_mock_generator(return_value: str) -> MagicMock:
    generator = MagicMock(spec=IDGenerator)
    generator.generate_id.return_value = return_value
    return generator
