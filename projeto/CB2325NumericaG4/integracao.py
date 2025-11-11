import math
import math, random

def integral_trap(funcao, a, b, n=1000):

    """
    Objetivos: - "Essa função calcula a integral numérica pelo método dos trapézios".   

    Parâmetros:     
    funcao: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.

    Retorna: "(float) Valor aproximado  da integral definida da função entre os limites a e b"
    """

    dx = (b-a)/n
    s = 0
    for c in range(n):
        s += (funcao(a + c*dx) + funcao(a + (c+1)*dx))*(dx/2)
    return s


def integral_rect(funcao, a, b, n=1000):

    """
    Objetivos: - "Essa função calcula a integral numérica por retângulos".   

    Parâmetros:     
    funcao: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.

    Retorna: "(float) Valor aproximado  da integral definida da função entre os limites a e b"
    """

    dx = (b-a)/n    
    s = 0
    for c in range(n):
        s += (funcao(a + c*dx))*dx
    return s

def integral_simpson(funcao, a, b, n=1000):

    """
    Objetivos: - "Essa função calcula a integral numérica pelo método de Simpson".   

    Parâmetros:     
    funcao: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.

    Retorna: "(float) Valor aproximado  da integral definida da função entre os limites a e b"
    """

    dx = (b-a)/n    
    s = 0
    for c in range(n):
        s += (funcao(a + c*dx) + 4 * funcao((a + a + c * dx + (c+1) * dx)/2) + funcao(a + (c+1)*dx))*(dx/6)         #Calcula as aproximações
    return s
    
def monteCarlo(a, b, c, d, funcao, n=1000):

    """
    Objetivos: - "Essa função calcula a integral numérica pelo método de Monte Carlo".   

    Parâmetros:     
    funcao: Função a ser integrada;  
    a (float): Limite inferior de integração;
    b (float): Limite superior de integração;  
    n (int): Número de subdivisões.

    Retorna: "(float) Valor aproximado  da integral definida da função entre os limites a e b"
    """

    s = 0
    for i in range(n):
        x = random.uniform(a, b)        #Escolhe a coordenada 
        y = random.uniform(c, d)
        s += funcao(x, y)
    
    media = s/n
    return media*(b-a)*(d-c)


def func_exemplo(a, b, c):  # Nome da função em letras minusculas utilizando snake_case
    
    """
    (Objetivo da função) - "Essa função faz isso utilizando esse método".   

    Parâmetros:     
    a (Tipo do parâmetro): Descrição do parâmetro;  
    b (Tipo do parâmetro): Descrição do parâmetro;  
    c (Tipo do parâmetro): Descrição do parâmetro.

    Retorna: "Aquilo que a função retorna"
    """

    return None

def test_integral_trap():
    assert abs(integral_trap(math.sin, 0, math.pi, 100000) - 2) < 1e-5
    assert abs(integral_trap(lambda x: x**2, 0, 1, 100000) - (1/3)) < 1e-5

def test_integral_rect():
    assert abs(integral_rect(math.sin, 0, math.pi, 100000) - 2) < 1e-5
    assert abs(integral_rect(lambda x: x**2, 0, 1, 100000) - (1/3)) < 1e-5

def test_integral_simpson():
    assert abs(integral_simpson(math.sin, 0, math.pi, 100000) - 2) < 1e-5
    assert abs(integral_simpson(lambda x: x**2, 0, 1, 100000) - (1/3)) < 1e-5

def test_monteCarlo():
    f = lambda x, y: x*y
    assert abs(monteCarlo(0, 1, 0, 1, f, 10000) - 0.25) < 1e-2
    g = lambda x, y: math.sin(x)*math.cos(y)
    assert abs(monteCarlo(0, math.pi/2, 0, math.pi/2, g, 10000) - 1) < 1e-2
