import random
import matplotlib.pyplot as plt
import numpy as np


Paleta = ["#084b83", "#680e4b", "#c42021", "#edae49"]


class IntegralNumerica:
    """
    Classe que representa uma integral numérica.

    Propriedades:
    func (Callable): A função integrada.
    valor (float): O valor computado da integral numérica.
    pontos (list[tuple]): Lista de pontos onde a função foi evaluada, na forma (x, f(x)).
    """

    def __init__(self, func, value, points):
        """
        Cria uma IntegralNumerica.

        Parâmetros:
        valor (float): O valor computado da integral numérica.
        pontos (list[tuple]): Lista de pontos onde a função foi evaluada, na forma (x, f(x)). 
        """
        self.func = func
        self.valor = value
        self.pontos = points
    
    def __repr__(self):
        return str(self.valor)
    
    def __getitem__(self, index):
        return self.points[index]
    

class IntegralReal(IntegralNumerica):
    """
    Representa uma integral numérica de uma função cujo domínio é os reais.

    Propriedades:
    min (float): O valor mínimo do domínio.
    max (float): O valor máximo do domínio.
    """

    def __init__(self, func, value, points, min, max):
        self.min = min
        self.max = max
        super().__init__(func, value, points)
    
    def create_plot(self, color=Paleta[0]):
        """
        Cria e retorna objetos de plotagem do matplotlib para a integral.

        Parâmetros:
        color (str): A cor da função.

        Retorna: tupla de objetos de figura e eixos do Matplotlib.
        """
        fig, ax = plt.subplots()
        X = np.linspace(self.min, self.max, 500)
        Y = self.func(X)
        ax.plot(X, Y, color=color, label="Curva")
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.set_title(f'Área computada: {self.valor:.4}')
        ax.grid(True)
        return fig, ax
    
    def plot_points(self, ax, color=Paleta[2]):
        """
        Adiciona os pontos da integral ao plot especificado.

        Parâmetros:
        ax: Objeto de eixos do Matplotlib.
        color (str): A cor dos pontos.
        """
        px, py = zip(*self.pontos)
        marker, stemlines, baseline = ax.stem(px, py, "--", label = "Pontos")
        plt.setp(marker, 'color', color)
        plt.setp(stemlines, 'color', color)
        plt.setp(baseline, 'color', color)


def integral_trap(funcao, a, b, n=1000) -> IntegralReal:
    """
    Objetivos: - "Essa função calcula a integral numérica pelo método dos trapézios".   

    Parâmetros:     
    funcao: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.

    Retorna: "(IntegralReal) Objeto representando o resultado da computação."
    """

    dx = (b-a)/n
    s = 0
    p = []
    for c in range(n):
        s += (funcao(a + c*dx) + funcao(a + (c+1)*dx))*(dx/2)
        p.append((a + c*dx, funcao(a + c*dx)))
    p.append((b, funcao(b)))
    return IntegralReal(funcao, s, p, a, b)


def plot_integral_trap(f, a, b, n=1000, simple=True, salvar_como=None) -> IntegralReal:
    """
    Calcula e plota a integral numérica pelo método dos trapézios.

    Parâmetros:     
    f: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.
    simple (bool): Se o gráfico gerado é simples; ou seja, se os pontos onde a integral foi computada são omitidos.
    salvar_como (str ou None): Caminho para salvar a image. Se None, apenas mostra o gráfico, sem salvar.

    Retorna: "(IntegralReal) Objeto representando o resultado da computação."
    """
    Paleta = ["#084b83", "#680e4b", "#c42021", "#edae49"]
    integral = integral_trap(f, a, b, n)

    fig, ax = integral.create_plot()
    px, py = zip(*integral.pontos)
    ax.plot(px, py, color = Paleta[1], label = "Aproximação")
    ax.fill_between(px, py, color = Paleta[1], alpha = 0.2)

    if not simple:
        integral.plot_points(ax)

    ax.legend()

    if salvar_como:
        try:
            fig.savefig(salvar_como)
            print(f"Gráfico salvo em: {salvar_como}")
        except Exception as e:
            print(f"Erro ao salvar o gráfico: {e}")

    plt.show()
    return integral


def integral_rect(funcao, a, b, n=1000) -> IntegralReal:

    """
    Objetivos: - "Essa função calcula a integral numérica por retângulos".   

    Parâmetros:     
    funcao: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.

    Retorna: "(IntegralReal) Objeto representando o resultado da computação."
    """

    dx = (b-a)/n    
    s = 0
    p = []
    for c in range(n):
        s += (funcao(a + c*dx))*dx
        p.append((a + c*dx, funcao(a + c*dx)))
    p.append((b, funcao(b)))
    return IntegralReal(funcao, s, p, a, b)


def plot_integral_rect(f, a, b, n=1000, simple=True, salvar_como=None) -> IntegralReal:
    """
    Calcula e plota a integral numérica pelo método dos retângulos.

    Parâmetros:     
    f: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.
    simple (bool): Se o gráfico gerado é simples; ou seja, se os pontos onde a integral foi computada são omitidos.
    salvar_como (str ou None): Caminho para salvar a image. Se None, apenas mostra o gráfico, sem salvar.

    Retorna: "(IntegralReal) Objeto representando o resultado da computação."
    """
    Paleta = ["#084b83", "#680e4b", "#c42021", "#edae49"]
    integral = integral_rect(f, a, b, n)

    fig, ax = integral.create_plot()
    dpx, dpy = [a], [0]
    for i in range(len(integral.pontos) - 1):
        # Para que o Matplotlib interprete nossos pontos como uma função escada,
        # para cada xi != b computado pelo método adicionamos os pontos
        # (xi, f(xi)) e (x(i + 1), f(xi)) ao nosso array.
        dpx += [integral.pontos[i][0], integral.pontos[i + 1][0]]
        dpy += [integral.pontos[i][1], integral.pontos[i][1]]
    dpx += [b]
    dpy += [0]
    ax.plot(dpx, dpy, color = Paleta[1], label = "Aproximação")
    ax.fill_between(dpx, dpy, color = Paleta[1], alpha = 0.2)

    if not simple:
        integral.plot_points(ax)

    ax.legend()

    if salvar_como:
        try:
            fig.savefig(salvar_como)
            print(f"Gráfico salvo em: {salvar_como}")
        except Exception as e:
            print(f"Erro ao salvar o gráfico: {e}")

    plt.show()
    return integral


def integral_simpson(funcao, a, b, n=1000) -> IntegralReal:
    """
    Objetivos: - "Essa função calcula a integral numérica pelo método de Simpson".   

    Parâmetros:     
    funcao: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.

    Retorna: "(IntegralReal) Objeto representando o resultado da computação."
    """

    dx = (b-a)/n    
    s = 0
    p = []
    for c in range(n):
        s += (funcao(a + c*dx) + 4 * funcao((a + a + c * dx + (c+1) * dx)/2) + funcao(a + (c+1)*dx))*(dx/6)         #Calcula as aproximações
        p += [
            (a + c*dx, funcao(a + c*dx)),
            ((a + a + c * dx + (c+1) * dx)/2, funcao((a + a + c * dx + (c+1) * dx)/2))
        ]
    p.append((b, funcao(b)))
    return IntegralReal(funcao, s, p, a, b)


def plot_integral_simpson(f, a, b, n=1000, simple=True, salvar_como=None) -> IntegralReal:
    """
    Calcula e plota a integral numérica pelo método de Simpson.

    Parâmetros:     
    f: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.
    simple (bool): Se o gráfico gerado é simples; ou seja, se os pontos onde a integral foi computada são omitidos.
    salvar_como (str ou None): Caminho para salvar a image. Se None, apenas mostra o gráfico, sem salvar.

    Retorna: "(IntegralReal) Objeto representando o resultado da computação."
    """
    integral = integral_simpson(f, a, b, n)

    def p2(x0, x1, x2, y0, y1, y2):
        L0x = lambda x: ((x - x1) * (x - x2)) / ((x0 - x1) * (x0 - x2))
        L1x = lambda x: ((x - x0) * (x - x2)) / ((x1 - x0) * (x1 - x2))
        L2x = lambda x: ((x - x0) * (x - x1)) / ((x2 - x0) * (x2 - x1))
        return lambda x: y0*L0x(x) + y1*L1x(x) + y2*L2x(x)

    fig, ax = integral.create_plot()
    lenp = len(integral.pontos) - 1 # "Distância" (em número de intervalos) entre o primeiro e último ponto no eixo x.
    factor = 50
    X = np.linspace(integral.min, integral.max, lenp * factor)
    Y = np.array([])
    for i in range(0, lenp - 1, 2):
        poly = p2(
            integral.pontos[i][0],
            integral.pontos[i + 1][0],
            integral.pontos[i + 2][0],
            integral.pontos[i][1],
            integral.pontos[i + 1][1],
            integral.pontos[i + 2][1],
        )
        Y = np.concatenate((
            Y, 
            poly(np.linspace(integral.pontos[i][0], integral.pontos[i + 2][0], 2 * factor)),
        ))
    ax.plot(X, Y, color = Paleta[1], label = "Aproximação")
    ax.fill_between(X, Y, color = Paleta[1], alpha = 0.2)

    if not simple:
        integral.plot_points(ax)

    ax.legend()

    if salvar_como:
        try:
            fig.savefig(salvar_como)
            print(f"Gráfico salvo em: {salvar_como}")
        except Exception as e:
            print(f"Erro ao salvar o gráfico: {e}")

    plt.show()
    return integral


def monteCarlo(a, b, c, d, funcao, n=1000):
    """
    Objetivos: - "Essa função calcula a integral numérica de uma função f : R² -> R pelo método de Monte Carlo."

    Parâmetros:     
    funcao: Função a ser integrada;  
    a (float): Limite inferior de integração na 1ª dimensão;
    b (float): Limite superior de integração na 1ª dimensão;
    c (float): Limite inferior de integração na 2ª dimensão;
    d (float): Limite superior de integração na 2ª dimensão;
    n (int): Número de repetições do experimento.

    Retorna: "(float) Valor aproximado da integral definida da função no quadrado especificado"
    """

    s = 0
    for i in range(n):
        x = random.uniform(a, b)       
        y = random.uniform(c, d)
        s += funcao(x, y)
    media = s/n
    return media*(b-a)*(d-c)


if __name__ == "__main__":
    print(plot_integral_rect(np.cos, 0, 4.5 * np.pi, n=40, simple=False))
    print(plot_integral_trap(np.cos, 0, 4.5 * np.pi, n=40, simple=False))
    print(plot_integral_simpson(np.cos, 0, 4.5 * np.pi, n=20, simple=False))
    print(plot_integral_simpson(np.cos, 0, 4.5 * np.pi, n=1000))
