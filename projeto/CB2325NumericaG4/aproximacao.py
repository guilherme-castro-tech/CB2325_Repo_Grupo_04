# Aproximação Funcional
# Alunos Responsáveis: Natan Spohr, Pedro Paulo


import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Poly
from scipy.optimize import minimize


def regressao_polinomial(pontos: list = None,
                         *,
                         grau: int = 1,
                         x: list = None,
                         y: list = None,
                         variavel: str = 'x',
                         decimais: int = 3):

    """
    Encontra a função polinomial que melhor aproxima um conjunto de pontos.
    Parâmetros:
        grau (inteiro positivo): Indica o grau do polinômio que vai aproximar os pontos;
        pontos (lista): Conjunto de pontos formados por duas coordenadas (x,y);
        x/y: (listas): Opção alternativa. Duas listas com as coordenadas x e y para cada ponto respectivamente;
        variavel: Usada na visualização do polinômio em forma de string;
        decimais: Casas de arredondamento dos valores de R² e na visualização do polinômio em forma de string.
    Retorna:
        Uma lista com os coeficientes do polinômio em ordem crescente de grau;
        Um float com o valor de R² da aproximação;
        A função obtida em forma de callable;
        A representação do polinômio em forma de string.
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
    if type(decimais) != int or decimais < 0:
        raise TypeError("Argumento 'decimais' deve ser inteiro não negativo")

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

    # String do Polinômio
    x = symbols(variavel)
    polinomio = [round(_, decimais) for _ in coeficientes]
    polinomio1 = Poly(reversed(polinomio), x)
    string = polinomio1.as_expr() #Monta a representação do polinômio para o título

    # Função
    f = lambda x: sum(coeficientes[i]*(x**i) for i in range(len(coeficientes)))

    return coeficientes, R_squared, f, string


def plot_regressao(pontos: list = None,
                              *,
                              grau: int = 1,
                              x: list = None,
                              y: list = None,
                              variavel: str = 'x',
                              decimais: int = 3,
                              tipo: str = "pol"):

    """
    Cria uma representação gráfica para uma aproximação polinomial de um conjunto de pontos.
    Parâmetros:
        grau (inteiro positivo): Indica o grau do polinômio que vai aproximar os pontos;
        pontos (lista): Conjunto de pontos formados por duas coordenadas (x,y);
        x/y: (listas): Opção alternativa. Duas listas com as coordenadas x e y para cada ponto respectivamente;
        variavel: Usada na visualização do polinômio em forma de string;
        decimais: Casas de arredondamento dos valores de R² e na visualização do polinômio em forma de string.
    Retorna:
        Uma imagem contendo os pontos fornecidos e o gráfico da aproximação.
    """

    if pontos:                          # Analisa se o método de imput escolhido foi a lista de pontos (x,y)
        if tipo == "pol":
            coeficientes, R_squared, f, string = regressao_polinomial(pontos, grau=grau, variavel=variavel, decimais=decimais)
        else:
            coeficientes, R_squared, f, string = regressao_nao_polinomial(pontos, variavel=variavel, decimais=decimais, tipo=tipo)
        xcoords, ycoords = zip(*pontos)
    elif x and y:                       # Analisa se o método de imput escolhido foi as listas de coordenadas em x e y
        if tipo == "pol":
            coeficientes, R_squared, f, string = regressao_polinomial(grau=grau, x=x, y=y, variavel=variavel, decimais=decimais)
        else:
            coeficientes, R_squared, f, string = regressao_nao_polinomial(x=x, y=y, variavel=variavel, decimais=decimais, tipo=tipo)
        xcoords, ycoords = x, y
    else:
        raise TypeError("Falta de argumentos obrigatórios -> 'pontos' ou ambos 'x' e 'y'")


    # Plotagem
    a, b = min(xcoords), max(xcoords)
    eixo_x = np.linspace(a, b, 200) # Cria pontos no eixo x no intervalo [a, b]
    eixo_y = f(eixo_x) # Encontra os pontos no eixo y
    plt.plot(eixo_x, eixo_y, color='#13505b', label='Curva') # Plota o gráfico
    plt.plot(xcoords, ycoords, 'o', color='#ed217c', label='Pontos') # Plota os pontos

    #Legendas
    if tipo == "pol":
        plt.title(f'Aproximação polinomial de grau {grau} (R² = {round(R_squared, decimais) if R_squared else None}) \n {string}')
    else:
        plt.title(f'Aproximação de função (R²={round(R_squared, decimais)}) \n {string}')
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.grid(True)
    plt.legend()
    plt.show()


def regressao_nao_polinomial(pontos: list = None,
              *,
              x: list = None,
              y: list = None,
              variavel: str = "x",
              decimais: int = 3,
              tipo: str = "sin"):
  
    """
    Encontra a função não polinomial que melhor aproxima um conjunto de pontos.
    Parâmetros:
        pontos (lista): Conjunto de pontos formados por duas coordenadas (x,y);
        x/y: (listas): Opção alternativa. Duas listas com as coordenadas x e y para cada ponto respectivamente;
        variavel: Usada na visualização da função em forma de string;
        decimais: Casas de arredondamento dos valores de R² e na visualização da função em forma de string;
        tipo: O modelo usado para aproximações -> Senoidal: sin, Exponencial: exp, Normal: normal.
    Retorna:
        Uma lista com os coeficientes obtidas pela aproximação;
        Um float com o valor de R² da aproximação;
        A função obtida em forma de callable;
        A representação da função em forma de string.
    """
  
    if pontos:                          # Analisa se o método de imput escolhido foi a lista de pontos (x,y)
        xcoords, ycoords = zip(*pontos)
    elif x and y:                       # Analisa se o método de imput escolhido foi as listas de coordenadas em x e y
        xcoords, ycoords = x, y
    else:
        raise TypeError("Falta de argumentos obrigatórios -> 'pontos' ou ambos 'x' e 'y'")
    if len(xcoords) != len(ycoords):
        raise ValueError("As listas de coordenadas não possuem o mesmo tamanho")
    if len(xcoords) != len(set(xcoords)):
        raise ValueError("Há diferentes pontos com mesma coordenada x")
    if type(decimais) != int or decimais < 0:
        raise TypeError("Argumento 'decimais' deve ser inteiro não negativo")


    if tipo == "sin": # a*sin(px+f)+b

        def func(valores, xcoords, ycoords):
            a, b, p, f = valores
            erros_quadrados = [(a*np.sin(p*xcoords[i]+f)+b-ycoords[i])**2 for i in range(len(xcoords))]
            return sum(erros_quadrados)

        def approx(xcoords, ycoords):
            parametros = minimize(func, x0=[1, 0, 1, 0], args=(xcoords, ycoords), bounds = [(0, None), (None, None), (None, None), (-np.pi, np.pi)])
            coef = parametros.x
            rss = parametros.fun
            rst = np.sum((ycoords - np.mean(ycoords)) ** 2)
            R_squared = 1 - rss/rst
            f = lambda x: coef[0]*np.sin(coef[2]*x+coef[3])+coef[1]
            string = f"{round(coef[0], decimais)}sin({round(coef[2], decimais)}{variavel}+{round(coef[3], decimais)})+{round(coef[1], decimais)}"
            return coef, R_squared, f, string

        return approx(xcoords, ycoords)


    if tipo == "exp": # a*e^(bx)
        def func(valores, xcoords, ycoords):
            a, b = valores
            erros_quadrados = [(a*np.exp(b*xcoords[i])-ycoords[i])**2 for i in range(len(xcoords))]
            return sum(erros_quadrados)

        def approx(xcoords, ycoords):
            parametros = minimize(func, x0=[1, 1], args=(xcoords, ycoords))
            coef = parametros.x
            rss = parametros.fun
            rst = np.sum((ycoords - np.mean(ycoords)) ** 2)
            R_squared = 1 - rss/rst
            f = lambda x: coef[0]*np.exp(coef[1]*x)
            string = f"{round(coef[0], decimais)}e^({round(coef[1], decimais)}{variavel})"
            return coef, R_squared, f, string

        return approx(xcoords, ycoords)
    

    if tipo == "normal": # a*e^(-(x+b)² / c)

        def func(valores, xcoords, ycoords):
            a, b, c = valores
            erros_quadrados = [(a*np.exp(-(xcoords[i]+b)**2 / c)-ycoords[i])**2 for i in range(len(xcoords))]
            return sum(erros_quadrados)

        def approx(xcoords, ycoords):
            parametros = minimize(func, x0=[10, 0, 10], args=(xcoords, ycoords), bounds = [(0, None), (None, None), (0, None)])
            coef = parametros.x
            rss = parametros.fun
            rst = np.sum((ycoords - np.mean(ycoords)) ** 2)
            R_squared = 1 - rss/rst
            f = lambda x: coef[0]*np.exp(-(x+coef[1])**2 / coef[2])
            string = f"{round(coef[0], decimais)}e^(-({variavel}+{round(coef[1], decimais)})² / {round(coef[2], decimais)})"
            return coef, R_squared, f, string

        return approx(xcoords, ycoords)

    raise ValueError("Tipo de aproximação não identificado")


if __name__ == '__main__':

    # Testes da regressão polinomial
    print('Teste 1:')
    pontos = [[1, 3], [2, 6], [3, 9]]
    plot_regressao(pontos, grau=1)
    print('Teste 2:')
    a = [1, 3, 6, 7]
    b = [1, 4, 9, 16]
    plot_regressao(grau=2, x=a, y=b, variavel='n', decimais=2)
    print('Teste 3:')
    pontos = [[0, 1], [1, 4], [2, 6], [3, 7], [4, 4], [5, 0], [6, 1]]
    plot_regressao(pontos, grau=4)

    # Testes da regressão não polinomial
    print("Teste 4:")
    pontos = [[0, 2.2], [0.5, 2.4], [1, 2.5], [1.2, 2.5], [1.8, 2.4], [2.2, 2.2], [2.5, 2], [2.9, 1.8], [3.5, 1.3], [4, 0.8]]
    plot_regressao(pontos, tipo="sin", variavel='t')
    print("Teste 5:")
    pontos = [[0, 5], [1, 6.5], [2, 7.5], [3, 9.5], [4, 12], [5, 13]]
    plot_regressao(pontos, tipo="exp", decimais=5)
    print("Teste 6:")
    pontos =[[-16, 7], [-10, 30], [-7, 45], [-5, 60], [2, 75], [6, 50], [14, 10]]
    plot_regressao(pontos, tipo="normal")
