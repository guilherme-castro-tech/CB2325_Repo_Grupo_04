# Aproximação Funcional
# Alunos Responsáveis: Natan Spohr, Pedro Paulo

import numpy as np
import matplotlib.pyplot as plt
  
def poly_regression(pontos: list, grau: int):
  
  '''Por enquanto o código apenas aceita uma lista de tuplas,
  e não uma lista para cada coordenada.'''
  x, y = zip(*pontos)

  # Passo a passo para regressão polinomial.
  # Leia-se @ como produto, .T como transposta.
  V = np.vander(x, grau+1, increasing=True) #Matriz de Vandermonde
  V1 = V.T @ V
  V2 = np.linalg.inv(V1)
  Y = V.T @ y
  coeficientes = V2 @ Y
  return coeficientes

# Teste de aproximação quadrática com 4 pontos
pontos = [(1, 3), (2, 4), (3, 7), (4, 5)]
print(poly_regression(pontos, 2))
