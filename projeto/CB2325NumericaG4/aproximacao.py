# Aproximação Funcional
# Alunos Responsáveis: Natan Spohr, Pedro Paulo

import numpy as np
import matplotlib.pyplot as plt
  
def poly_regression(grau: int = 1, pontos: list = None, *, x: list = None, y: list = None):
  if pontos:
    xcords, ycords = zip(*pontos)
  elif x and y:
    xcords, ycords = x, y
  else:
    raise TypeError("Falta de argumentos obrigatórios -> 'pontos' ou ambos 'x' e 'y'")
  
  if type(grau) != int or grau < 0:
    raise TypeError("Argumento 'grau' deve ser inteiro não negativo")

  # Passo a passo para regressão polinomial.
  # Leia-se @ como produto, .T como transposta.
  V = np.vander(xcords, grau+1, increasing=True) # Matriz de Vandermonde
  V1 = V.T @ V
  V2 = np.linalg.inv(V1)
  Y = V.T @ ycords
  coeficientes = V2 @ Y
  return coeficientes

# Testes
pontos = [(1, 3), (2, 4), (3, 7), (4, 5)]
print(poly_regression(2, pontos))
a = [1, 2, 3, 4]
b = [1, 4, 9, 16]
print(poly_regression(1, x=a, y=b))
