import numpy as np
import pytest
from interpolacao import Linear_Interp


@pytest.fixture
def interp():
    x = [0, 1, 3, 4, 6]
    y = [0, 2, 1, 5, 4]
    return Linear_Interp(x, y)


def test_pontos_conhecidos(interp):
    assert interp(0) == 0
    assert interp(3) == 1
    assert interp(6) == 4


def test_interpolacao_intermediaria(interp):
    assert interp(0.5) == 1          # metade entre 0 e 2
    assert pytest.approx(interp(2.0), rel=1e-6) == 1.5
    assert pytest.approx(interp(5.0), rel=1e-6) == 4.5


def test_interpolacao_vetor(interp):
    pontos = np.array([0.0, 1.0, 3.0, 6.0])
    esperado = np.array([0.0, 2.0, 1.0, 4.0])
    resultado = interp(pontos)
    assert np.allclose(resultado, esperado)


def test_extrapolacao(interp):
    assert interp(-1.0) is None
    assert interp(7.0) is None

def test_valores_x_repetidos():
    x = [0, 2, 2, 4]
    y = [0, 1, 3, 4]
    interp = Linear_Interp(x, y)

    assert interp(2) == 1  # Deve pegar o primeiro y associado ao x=2

def test_valor_exato_no_ponto(interp):
    assert interp(1) == 2       # já existe no conjunto
    assert interp(4) == 5

def test_limite_superior(interp):
    assert interp(interp.x[-1]) == interp.y[-1]

def test_interpolacao_lista(interp):
    pontos = [0, 1, 3, 6]
    esperado = np.array([0, 2, 1, 4])
    resultado = interp(pontos)
    assert np.allclose(resultado, esperado)


