import numpy as np
import pytest
from interpolacao import Hermite_Interp

@pytest.fixture
def interp():
    x = [0, 1, 3, 4, 6]
    y = [0, 1, 9, 16, 36]
    dy = [0, 2, 6, 8, 12]
    return Hermite_Interp(x, y, dy)

def test_pontos_conhecidos(interp):
    assert interp(0) == pytest.approx(0, rel=1e-10)
    assert interp(3) == pytest.approx(9, rel=1e-10)
    assert interp(6) == pytest.approx(36, rel=1e-10)

def test_interpolacao_intermediaria(interp):
    assert pytest.approx(interp(1.0), rel=1e-6) == 1.0
    assert pytest.approx(interp(2.0), rel=1e-6) == 4.0
    assert pytest.approx(interp(5.0), rel=1e-6) == 25.0      

def test_interpolacao_vetor(interp):
    pontos = np.array([0.0, 1.0, 3.0, 6.0])
    esperado = np.array([0.0, 1.0, 9.0, 36.0])
    resultado = interp(pontos)
    assert np.allclose(resultado, esperado)

def test_extrapolacao(interp):
    assert interp(-1.0) is None
    assert interp(7.0) is None  

def test_valores_x_repetidos():
    x = [0, 1, 2, 4]
    y = [0, 1, 4, 16]
    dy = [0, 1, 4, 8]
    interp = Hermite_Interp(x, y, dy)

    assert interp(2) == 4  

def test_valor_exato_no_ponto(interp):
    resultado = interp(1)
    if isinstance(resultado, np.ndarray) and resultado.size == 1:
        resultado = resultado.item()
    assert resultado == pytest.approx(1, rel=1e-10)  

def test_limite_superior(interp):
    resultado = interp(interp.x[-1])
    esperado = interp.y[-1]
    
    if isinstance(resultado, np.ndarray) and resultado.size == 1:
        resultado = resultado.item()
    if isinstance(esperado, np.ndarray) and esperado.size == 1:
        esperado = esperado.item()
        
    assert resultado == pytest.approx(esperado, rel=1e-10)  


def test_interpolacao_lista(interp):
    pontos = [0, 1, 3, 6]
    esperado = np.array([0, 1, 9, 36])
    resultado = interp(pontos)
    assert np.allclose(resultado, esperado)