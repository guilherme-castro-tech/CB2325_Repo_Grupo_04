from integracao import integral_trap, integral_rect, integral_simpson, monteCarlo
import math
import pytest


def test_integral_trap():
    assert abs(integral_trap(math.sin, 0, math.pi, 100000) - 2) < 1e-5
    assert abs(integral_trap(lambda x: x**2, 0, 1, 100000) - (1/3)) < 1e-5

def test_integral_rect():
    assert abs(integral_rect(math.sin, 0, math.pi, 100000) - 2) < 1e-5
    assert abs(integral_rect(lambda x: x**2, 0, 1, 100000) - (1/3)) < 1e-5

def test_integral_simpson():
    assert abs(integral_simpson(math.sin, 0, math.pi, 100000) - 2) < 1e-5
    assert abs(integral_simpson(lambda x: x**2, 0, 1, 100000) - (1/3)) < 1e-5

def test_monteCarlo():
    f = lambda x, y: x*y
    assert abs(monteCarlo(0, 1, 0, 1, f, 10000) - 0.25) < 1e-2
    g = lambda x, y: math.sin(x)*math.cos(y)
    assert abs(monteCarlo(0, math.pi/2, 0, math.pi/2, g, 10000) - 1) < 1e-2
