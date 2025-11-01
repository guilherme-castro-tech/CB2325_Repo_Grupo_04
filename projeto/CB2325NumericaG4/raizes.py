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

def metodo_da_secante(f, a, b, tol):
    return "Em andamento"

def metodo_de_newton(f, a, b, tol):
    return "Em andamento"

# Plotagem:

def plotagem(f, a: float, b: float, aproximacoes: list, raiz: float, method=None):

    """
    Objetivo:
        Criar uma representação gráfica das aproximação feitas para encontar a raiz 

    Parâmetros:
        f (função): função contínua
        a, b (float): extremos do intervalo [a, b]
        raiz: valor x tal que f(x) == 0
        aproximacoes: lista que guarda os pontos de aproximações para encontrar a raiz
        method: o método escolhido para encontrar a raiz
    """

    # Eixos: 
    valores_x = np.linspace(a - 1, b + 1, 200)  # eixo x
    valores_y = [f(x) for x in valores_x]  # eixo y

    plt.plot(valores_x, valores_y, label="Curva f(x)", color="#13505B")
    plt.axhline(0, color="black", linewidth=1)
 
    # Marcação das aproximações:
    plt.scatter(aproximacoes, [f(x) for x in aproximacoes], color="#0C7489", label="Aproximações")
    plt.scatter(raiz, f(raiz), color="#ED217C", label="Raiz final", zorder=5)

    # Plotagem:
    nomes = {"bissecao": "Bisseção", "secante": "Secante", "newton": "Newton"}

    plt.title(f"Método da {nomes[method]}")
    plt.xlabel("Eixo X")
    plt.ylabel("Eixo Y")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.show()

# Função principal:

def raiz(f, a: float, b: float, tol=1e-6, method=None):

    """
    Objetivo:
        Executar um método numérico para encontrar uma raiz de f(x) 
        no intervalo [a, b] e exibir o gráfico do processo.
          
    Parâmetros:
        f (função): função contínua
        a, b (float): extremos do intervalo [a, b]
        tol (float): precisão
        method (str): nome do método ("bissecao", "secante" ou "newton")

    Retorno:
        Valor aproximado da raiz (float)
    """

    if method == "bissecao":
        raiz, aprox = metodo_da_bissecao(f, a, b, tol)
        if raiz is not None:
            plotagem(f, a, b, aprox, raiz, method="bissecao")
        return raiz
    
    elif method == "secante":
        raiz, aprox = metodo_da_secante(f, a, b, tol)
        plotagem(f, a, b, aprox, raiz, method="secante")
        return raiz
    
    elif method == "newton":
        raiz, aprox = metodo_de_newton(f, a, b, tol)
        plotagem(f, a, b, aprox, raiz, method="newton")
        return raiz
    
    else:
        raise ValueError("Método inválido!")
    
# Exemplos provisórios (por enquanto só para o método da bisseção):

if __name__ == "__main__":

    f1 = lambda x: math.exp(-x) - x
    print("  Exemplo 1 (raiz decimal infinita)  ".center(100, "─"))
    print("\nFunção: f(x) = e⁻ˣ-x")
    print("Intervalo: [0, 1]\n")
    print(f"Raiz aproximada pelo Método da Bisseção: {raiz(f1, 0, 1, method='bissecao'):.3f}\n")  # resposta esperada: ≈ 0.567

    f2 = lambda x: x**2 - 4
    print("  Exemplo 2 (raiz exata)  ".center(100, "─"))
    print("\nFunção: f(x) = x²-4")
    print("Intervalo: [1, 3]\n")
    print(f"Raiz pelo Método da Bisseção: {raiz(f2, 1, 3, method='bissecao'):.1f}\n")  # resposta esperada: = 2 

    f3 = lambda x: abs(x)
    print("  Exemplo 3 (há raiz, mas o Método da Bisseção não calcula)  ".center(100, "─"))
    print("\nFunção: f(x) = |x|")
    print("Intervalo: [-1, 1]\n")
    print(f"Raiz pelo Método da Bisseção: {raiz(f3, -1, 1, method='bissecao')}\n")  # resposta esperada: None

    f4 = lambda x: x**2 + 4
    print("  Exemplo 4 (não há raízes)  ".center(100, "─"))
    print("\nFunção: f(x) = x²+4")
    print("Intervalo: [-2, 2]\n")
    print(f"Raiz pelo Método da Bisseção: {raiz(f4, -2, 2, method='bissecao')}\n")  # resposta esperada: None

