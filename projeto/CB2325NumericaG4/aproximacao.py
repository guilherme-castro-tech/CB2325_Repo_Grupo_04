# Aproximação Funcional
# Alunos Responsáveis: Natan Spohr, Pedro Paulo


import numpy as np
import matplotlib.pyplot as plt
def regressao_polinomial(grau: int = 1,
                         pontos: list = None,
                         *,
                         x: list = None,
                         y: list = None):

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
        raise ValueError("As listas de coordenadas não possuem o mesmo tamanho")
    if grau >= len(xcoords):
        raise ValueError("Argumento 'grau' é maior ou igual ao número de pontos. Não há solução única para o sistema")
    if len(xcoords) != len(set(xcoords)):
        raise ValueError("Há diferentes pontos com mesma coordenada x")

    # Passo a passo para regressão polinomial (Mínimos quadrados)
    # coeficientes = (V^T * V)^{-1} * V^T * ycords
    # Leia-se @ como produto, .T como transposta
    V = np.vander(xcoords, grau+1, increasing=True) # Cria uma matriz de Vandermonde
    V1 = V.T @ V
    Y = V.T @ ycoords
    coeficientes = np.linalg.solve(V1, Y) # Encontra os coeficientes através de decomposição LU

    # Cálculo do R²
    y_aproximados = V @ coeficientes
    rss = np.sum((ycoords - y_aproximados)**2)
    rst = np.sum((ycoords - np.mean(ycoords)) ** 2)
    if rst == 0:
      R_squared = None
    else:
      R_squared = 1-rss/rst

    return coeficientes, R_squared


def plot_regressao_polinomial(grau: int = 1,
                              pontos: list = None,
                              *,
                              x: list = None,
                              y: list = None,
                              variavel: str = 'x',
                              decimais: int = 3):

    """
    Cria uma representação gráfica para uma aproximação polinomial de um conjunto de pontos.
    Parâmetros:
        grau (inteiro positivo): Indica o grau do polinômio que vai aproximar os pontos;
        pontos (lista): Conjunto de pontos formados por duas coordenadas (x,y);
        x/y: (listas): Opção alternativa. Duas listas com as coordenadas x e y para cada ponto respectivamente.
    Retorna: Uma imagem contendo os pontos fornecidos e o gráfico da aproximação.
    """

    if pontos:                          # Analisa se o método de imput escolhido foi a lista de pontos (x,y)
        coeficientes, R_squared = regressao_polinomial(grau, pontos)
        xcoords, ycoords = zip(*pontos)
    elif x and y:                       # Analisa se o método de imput escolhido foi as listas de coordenadas em x e y
        coeficientes, R_squared = regressao_polinomial(grau, x=x, y=y)
        xcoords, ycoords = x, y
    else:
        raise TypeError("Falta de argumentos obrigatórios -> 'pontos' ou ambos 'x' e 'y'")
    if type(decimais) != int or decimais < 0:
        raise TypeError("Argumento 'decimais' deve ser inteiro não negativo")


    # Plotagem
    a, b = min(xcoords), max(xcoords)
    eixo_x = np.linspace(a, b, 200) # Cria pontos no eixo x no intervalo [a, b]
    eixo_y = np.zeros_like(eixo_x)
    for i in range(len(coeficientes)): # Encontra os pontos no eixo y
        eixo_y += coeficientes[i]*(eixo_x**i)
    plt.plot(eixo_x, eixo_y, color='#13505b', label='Curva') # Plota o gráfico
    plt.plot(xcoords, ycoords, 'o', color='#ed217c', label='Pontos') # Plota os pontos


    #Legendas
    from sympy import symbols, Poly
    x = symbols(variavel)
    polinomio = [round(_, decimais) for _ in coeficientes]
    polinomio1 = Poly(reversed(polinomio), x)
    polinomio2 = polinomio1.as_expr() #Monta a representação do polinômio para o título
    plt.title(f'Aproximação polinomial de grau {grau} (R² = {round(R_squared, decimais) if R_squared else None}) \n {polinomio2}')
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    #Testes
    print('Teste 1:')
    pontos = [[1, 3], [2, 6], [3, 9]]
    print("Pontos: ", regressao_polinomial(1, pontos)[0])
    plot_regressao_polinomial(1, pontos)
    print('Teste 2:')
    a = [1, 3, 6, 7]
    b = [1, 4, 9, 16]
    print("Pontos: ", regressao_polinomial(2, x=a, y=b)[0])
    print("R² = ", regressao_polinomial(2, x=a, y=b)[1])
    plot_regressao_polinomial(2, x=a, y=b, variavel='n', decimais=2)
