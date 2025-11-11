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
