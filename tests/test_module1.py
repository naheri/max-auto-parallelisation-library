import pytest
from ma_librairie.module1 import addition

def test_addition():
    assert addition(2, 3) == 5
    assert addition(-1, 1) == 0
