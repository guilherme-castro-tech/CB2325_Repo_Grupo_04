# Importações:
import math
import numpy as np
import matplotlib.pyplot as plt

# Funções auxiliares:
def derivada(f, x, h=1e-6):

    """
    Função que calcula a primeira derivada de f(x) em um ponto x usando o
    método de diferenças centrais.
        
    Parâmetros: 
        f (função): função contínua;
        x (float): ponto oem que a derivada será calculada;
        h (float): precisão

    Retorna: Valor aproximado da derivada de f(x) no ponto x (float).
    """

    return (f(x + h) - f(x - h)) / (2 * h)

# Métodos numéricos para encontrar raízes de funções reais:
def metodo_da_bissecao(f, a: float, b: float, tol=1e-6):

    """
    Função que determina uma raiz real de f(x) no intervalo [a, b] pelo método da bisseção.
        
    Parâmetros: 
        f (função): função contínua;
        a, b (float): extremos do intervalo [a, b];
        tol (float): precisão.

    Retorna: Valor aproximado da raiz de f(x), com precisão 10⁻⁶ (float), e lista de aproximações. 
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
            c = (a + b) / 2  # Ponto médio
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

def metodo_de_newton_raphson(f, a: float, b: float, tol):

    """
    Função que determina uma raiz real de f(x) no intervalo [a, b] pelo método de Newton Raphson.
    
    Parâmetros: 
        f (função): função contínua;
        a, b (float): extremos do intervalo [a, b];
        tol (float): precisão.

    Retorna: Valor aproximado da raiz de f(x), com precisão 10⁻⁶ (float), e lista de aproximações. 
    Retorna (None, []) se não houver mudança de sinal no intervalo.
    """

	# Inicializa xn como o extremo inicial do intervalo 'a'.
    xn = a
	
	# Condição para do loop (while).
    passo = False

	# Cria uma lista, originalmente vazia, para adicionar posteriormente os pontos percorridos 
    # durante a aproximação.
    aprox = []
	
	# Inicializa a variável raiz.
    raiz = None

    while passo == False:
		# Calcula a derivada de f(x)
        df_dx = derivada(f, xn, h=tol)

		# Verifica se a derivada é válida ou não.
        if abs(df_dx) < tol:
			# A derivada não é válida.
            passo = True
            return None, aprox
        
        else:
			# A derivada é válida.
			# Verifica se 'a' (extremo inicial do intervalo) é uma raiz.
            if abs(f(a)) <= tol:
                raiz = a

			# Verifica se 'b' (extremo final do intervalo) é uma raiz.
            elif abs(f(b)) <= tol:
                raiz = b

            else:
				# Considere xm como o valor seguinte para x a ser verificado depois de xn.
                xm = xn - (f(xn) / df_dx)

				# Verifica se xm pertence ao intevalo [a, b].
                if a <= xm <= b:
					# xm pertence ao intevalo [a, b].
					# Verifica se 'xm' é uma raiz.
                    if abs(f(xm)) <= tol:
                        raiz = xm
                        passo = True

                    else:
						# Adiciona xm na list de pontos percorridos.
                        aprox.append(xn)
						# xn armazena o valor de xm para calcular o próximo valor para x.
                        xn = xm

                else:
					# xm não pertence ao intevalo [a, b].
                    passo = True
                    return None, aprox

    return raiz, aprox # Retorna a raiz e a lista de pontos percorridos.

# Plotagem dos gráficos:
def plotagem_raiz(f, a: float, b: float, tol=1e-6, method=None):

    """
    Função que cria uma representação gráfica das aproximação feitas para encontar a raiz.

    Parâmetros:
        f (função): função contínua;
        a, b (float): extremos do intervalo [a, b];
        tol (float): precisão;
        method: o método escolhido para encontrar a raiz.

    Retorna: Uma imagem contendo a função, as aproximações feitas e a raiz.
    """

    # Determinação do valor da raiz (float) e dos pontos de aproximação (list):
    if method == "bissecao":
        raiz, aprox = metodo_da_bissecao(f, a, b, tol)
        if raiz is None:
            raise ValueError('Não é possível plotar o gráfico.')
    
    elif method == "secante":
        raiz, aprox = metodo_da_secante(f, a, b, tol)
        if raiz is None:
            raise ValueError('Não é possível plotar o gráfico.')
    
    elif method == "newton_raphson":
        raiz, aprox = metodo_de_newton_raphson(f, a, b, tol)
        if raiz is None:
            raise ValueError('Não é possível plotar o gráfico.')
    
    else:
        raise ValueError("Método inválido!")
    
    # Paleta de cores padrão definida pelo grupo:
    Paleta = ["#084b83", "#680e4b", "#c42021", "#edae49"]
    
    # Eixos: 
    valores_x = np.linspace(a - 1, b + 1, 200)  # eixo x
    valores_y = [f(x) for x in valores_x]  # eixo y

    # Curva:
    plt.plot(valores_x, valores_y, label="Curva f(x)", color=Paleta[0])

    # Destaque do eixo x:
    plt.axhline(0, color="grey")
 
    # Marcação dos pontos da lista de aproximações:
    plt.scatter(aprox, [f(x) for x in aprox], color=Paleta[2], label="Aproximações", zorder=5)
    
    # Marcação da raiz:
    if raiz is not None:
        plt.scatter(raiz, f(raiz), color=Paleta[3], label="Raiz final", zorder=5)

    # Plotagem:
    nomes = {"bissecao": "Bisseção", "secante": "Secante", "newton_raphson": "Newton-Raphson"}

    plt.title(f"Método da {nomes[method]}")
    plt.xlabel("Eixo X")
    plt.ylabel("Eixo Y")
    plt.grid(True)
    plt.legend()
    plt.show()

# Função principal:
def raiz(f, a: float, b: float, tol=1e-6, method=None):

    """
    Função que executa um método numérico para encontrar uma raiz de f(x) 
    no intervalo [a, b].

    Parâmetros:
        f (função): função contínua;
        a, b (float): extremos do intervalo [a, b];
        tol (float): precisão;
        method (str): nome do método ("bissecao", "secante" ou "newton").

    Retorna: Valor aproximado da raiz (float).
    """

    if method == "bissecao":
        raiz = metodo_da_bissecao(f, a, b, tol)[0]
        return raiz
    
    elif method == "secante":
        raiz = metodo_da_secante(f, a, b, tol)[0]
        return raiz
    
    elif method == "newton_raphson":
        raiz = metodo_de_newton_raphson(f, a, b, tol)[0]
        return raiz
    
    else:
        raise ValueError("Método inválido!")
    
# Exemplos:
if __name__ == "__main__":
    
    # Exemplo 1
    # Função e intervalo:
    f1 = lambda x: math.exp(-x) - x
    print("  Exemplo 1 (raiz decimal infinita)  ".center(100, "─"))
    print("\nFunção: f(x) = e⁻ˣ-x")
    print("Intervalo: [0, 1]")

    # Métodos:
    print(f"Raiz aproximada pelo Método da Bisseção: {raiz(f1, 0, 1, 1e-6, method='bissecao'):.3f}")  # Resposta esperada: ≈ 0.567
    print(f"Raiz aproximada pelo Método da Newton-Raphson: {raiz(f1, 0, 1, 1e-6, method='newton_raphson'):.3f}\n") # Resposta esperada: ≈ 0.567

    # Plotagens:
    plotagem_raiz(f1, a=0, b=1, tol=1e-6, method='bissecao')
    plotagem_raiz(f1, a=0, b=1, tol=1e-6, method='newton_raphson')


    # Exemplo 2
    # Função e intervalo:
    f2 = lambda x: x**2 - 4
    print("  Exemplo 2 (raiz exata)  ".center(100, "─"))
    print("\nFunção: f(x) = x²-4")
    print("Intervalo: [1, 3]\n")
    
    # Métodos:
    print(f"Raiz pelo Método da Bisseção: {raiz(f2, 1, 3, 1e-6, method='bissecao'):.1f}")  # Resposta esperada: 2.0
    print(f"Raiz aproximada pelo Método da Newton-Raphson: {raiz(f2, 1, 3, 1e-6, method='newton_raphson'):.1f}\n") # Resposta esperada: 2.0

    # Plotagens:
    plotagem_raiz(f2, a=1, b=3, tol=1e-6, method='bissecao')
    plotagem_raiz(f2, a=1, b=3, tol=1e-6, method='newton_raphson')


    # Exemplo 3
    # Função e intervalo:
    f3 = lambda x: abs(x)
    print("  Exemplo 3 (há raiz, mas a imagem não muda de sinal)  ".center(100, "─"))
    print("\nFunção: f(x) = |x|")
    print("Intervalo: [-1, 1]\n")

    # Métodos:
    print(f"Raiz pelo Método da Bisseção: {raiz(f3, -1, 1, 1e-6, method='bissecao')}")  # Resposta esperada: None
    print(f"Raiz aproximada pelo Método da Newton-Raphson: {raiz(f3, -1, 1, 1e-6, method='newton_raphson'):.1f}\n")  # Resposta esperada: 0.0

    # Plotagem:
    plotagem_raiz(f3, a=-1, b=1, tol=1e-6, method='newton_raphson')


    # Exemplo 4
    # Função e intervalo:
    f4 = lambda x: x**2 + 4
    print("  Exemplo 4 (não há raízes)  ".center(100, "─"))
    print("\nFunção: f(x) = x²+4")
    print("Intervalo: [-2, 2]\n")

    # Métodos:
    print(f"Raiz pelo Método da Bisseção: {raiz(f4, -2, 2, 1e-6, method='bissecao')}")  # resposta esperada: None
    print(f"Raiz pelo Método da Newton-Raphson: {raiz(f4, -2, 2, 1e-6, method='newton_raphson')}\n")  # resposta esperada: None