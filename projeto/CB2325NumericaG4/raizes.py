# Importações:

import math
import numpy as np
import matplotlib.pyplot as plt

# Métodos:

def metodo_da_bissecao(f, a: float, b: float, tol=1e-6):

    """
    Objetivo: 
        Determinar uma raiz real de f(x) no intervalo [a, b] pelo método da bisseção. 
        
    Parâmetros: 
        f (função): função contínua 
        a, b (float): extremos do intervalo [a, b] 
        tol (float): precisão 

    Retorno: 
        Valor aproximado da raiz de f(x), com precisão 10⁻⁶ (float), e lista de aproximações. 
        Retorna (None, []) se não houver mudança de sinal no intervalo.
    """
    
    aproximacoes = []

    # Caso em que não é possível determinar a raiz, pois f(a) e f(b) têm o mesmo sinal:
    if f(a) * f(b) > 0:
        return None, aproximacoes
		
    # Caso em que um dos extremos é a raiz:
    if f(a) == 0:
        raiz = a
    elif f(b) == 0:
        raiz = b
    else:
        # Caso em que a raiz pertence ao intervalo (a, b):
        while abs(b - a) >= tol:
            c = (a + b) / 2  # ponto médio
            aproximacoes.append(c)

            if f(c) == 0:
                raiz = c
                break
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
    raiz = c

    return raiz, aproximacoes