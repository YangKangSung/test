import time
import pytest


def test_fast():
    time.sleep(0.1)
    assert True


def test_medium():
    time.sleep(0.5)
    assert True


def test_slow():
    time.sleep(1.0)
    assert True


def test_fail():
    time.sleep(0.2)
    assert False
