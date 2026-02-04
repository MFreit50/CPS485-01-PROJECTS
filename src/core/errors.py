class VisualizationEngineError(Exception):
    """Base class for all framework level errors."""
    pass

class ContractViolationError(VisualizationEngineError):
    """Raised when a contract between components is violated."""
    pass

class InvalidLifecycleStateError(ContractViolationError):
    """Raised when an object is used in an invalid lifecycle state."""
    pass

class InvalidEventError(ContractViolationError):
    """Raised when an event does not conform to expected structure or data."""
    pass