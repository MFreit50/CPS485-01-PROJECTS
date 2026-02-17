import pytest
from src.core.time.simple_clock import SimpleClock
from src.core.errors import InvalidLifecycleError

def test_clock_starts_at_zero():
    clock = SimpleClock()
    assert clock.now() == 0

def test_tick_advances_time():
    clock = SimpleClock()
    assert clock.tick() == 1
    assert clock.tick() == 2

def test_now_does_not_advance():
    clock = SimpleClock()
    clock.tick()
    assert clock.now() == 1