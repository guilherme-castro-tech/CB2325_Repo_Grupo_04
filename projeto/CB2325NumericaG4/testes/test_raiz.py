import math
import pytest
from CB2325_Repo_Grupo_04.projeto.CB2325NumericaG4.raizes import raiz

tol = 1e-6  # Precisão

def test_exemplo1(): # Há uma raiz não exata (decimal infinito)
    f1 = lambda x: math.exp(-x) - x
    
    resultado_bissecao = raiz(f1, 0, 1, tol, method='bissecao')
    assert math.isclose(resultado_bissecao, 0.567, abs_tol=1e-3)
    resultado_newton = raiz(f1, 0, 1, tol, method='newton_raphson')
    assert math.isclose(resultado_newton, 0.567, abs_tol=1e-3)

def test_exemplo2(): # Há uma raiz exata
    f2 = lambda x: x**2 - 4
    
    resultado_bissecao = raiz(f2, 1, 3, tol, method='bissecao')
    assert math.isclose(resultado_bissecao, 2.0, abs_tol=1e-3)
    resultado_newton = raiz(f2, 1, 3, tol, method='newton_raphson') 
    assert math.isclose(resultado_newton, 2.0, abs_tol=1e-3)

def test_exemplo3(): # Existe uma raiz, mas não há mudança de sinal da imagem
    f3 = lambda x: abs(x)
    
    resultado_bissecao = raiz(f3, -1, 1, tol, method='bissecao')
    assert resultado_bissecao is None
    resultado_newton = raiz(f3, -1, 1, tol, method='newton_raphson')
    assert math.isclose(resultado_newton, 0.0, abs_tol=1e-3)
    
def test_exemplo4(): # Não há raízes
    f4 = lambda x: x**2 + 4
    
    resultado_bissecao = raiz(f4, -2, 2, tol, method='bissecao')
    assert resultado_bissecao is None
    resultado_newton = raiz(f4, -2, 2, tol, method='newton_raphson')
    assert resultado_newton is None