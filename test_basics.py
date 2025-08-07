
import pytest

# Sample functions to test
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def is_game_over(score, max_score):
    return score >= max_score

# Test cases
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 4) == -4
    assert subtract(-2, -2) == 0

def test_is_game_over():
    assert is_game_over(10, 10) is True
    assert is_game_over(9, 10) is False
    assert is_game_over(15, 10) is True
