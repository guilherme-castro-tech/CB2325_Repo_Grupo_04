# Aproximação Funcional
# Alunos Responsáveis: Natan Spohr, Pedro Paulo

import numpy as np
import matplotlib.pyplot as plt

def regressao_polinomial(grau: int = 1, pontos: list = None, *, x: list = None, y: list = None):

    """
    Encontra a função polinomial que melhor aproxima um conjunto de pontos.

    Parâmetros:     
        grau (inteiro positivo): Indica o grau do polinômio que vai aproximar os pontos;    
        pontos (lista): Conjunto de pontos formados por duas coordenadas (x,y);     
        x/y: (listas): Opção alternativa. Duas listas com as coordenadas x e y para cada ponto respectivamente.

    Retorna: Uma lista com os coeficientes do polinômio em ordem crescente de grau.
    """

    if pontos:                          # Analisa se o método de imput escolhido foi a lista de pontos (x,y)
        xcoords, ycoords = zip(*pontos)
    elif x and y:                       # Analisa se o método de imput escolhido foi as listas de coordenadas em x e y
        xcoords, ycoords = x, y
    else:
        raise TypeError("Falta de argumentos obrigatórios -> 'pontos' ou ambos 'x' e 'y'")

    if type(grau) != int or grau < 0:
        raise TypeError("Argumento 'grau' deve ser inteiro não negativo")
    
    if len(xcoords) != len(ycoords):
        raise ValueError("As listas de coordenadas devem ter o mesmo tamanho")

    # Passo a passo para regressão polinomial (Mínimos quadrados).
    # coeficientes = (V^T * V)^{-1} * V^T * ycords
    # Leia-se @ como produto, .T como transposta.

    V = np.vander(xcoords, grau+1, increasing=True) # Cria uma matriz de Vandermonde
    V1 = V.T @ V                                    
    V2 = np.linalg.inv(V1)  # Inverte a matriz V1
    Y = V.T @ ycoords                                
    coeficientes = V2 @ Y   # Encontra os coeficientes
    return coeficientes

def plot_regressao_polinomial(grau: int = 1, pontos: list = None, *, x: list = None, y: list = None):

    """
    Cria uma representação gráfica para uma aproximação polinomial de um conjunto de pontos.

    Parâmetros:     
        grau (inteiro positivo): Indica o grau do polinômio que vai aproximar os pontos;    
        pontos (lista): Conjunto de pontos formados por duas coordenadas (x,y);     
        x/y: (listas): Opção alternativa. Duas listas com as coordenadas x e y para cada ponto respectivamente.
    
    Retorna: Uma imagem contendo os pontos fornecidos e o gráfico da aproximação.
    """

    #Implementar a função utilizando o matplotlib

if __name__ == '__main__':
    
    #Testes:
    print('Teste 1:')
    pontos = [[1, 3], [2, 4], [3, 7], [4, 5]]
    print(regressao_polinomial(2, pontos))

    print('Teste 2:')
    a = [1, 2, 3, 4]
    b = [1, 4, 9, 16]
    print(regressao_polinomial(2, x=a, y=b))
