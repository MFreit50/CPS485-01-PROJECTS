from src.core.contracts.event import Event


class SentinelStopSignal(Event):
    """
    Sentinel object used to signal worker threads to stop processing events.
    This is a unique object that can be placed in the event queue to indicate
    that workers should exit their processing loops gracefully.
    """

    def __init__(self, timestamp=0, producer_id="sentinel_stop_signal"):
        super().__init__(timestamp=timestamp, producer_id=producer_id)

    @property
    def event_id(self) -> str:
        return "sentinel_stop_signal"
