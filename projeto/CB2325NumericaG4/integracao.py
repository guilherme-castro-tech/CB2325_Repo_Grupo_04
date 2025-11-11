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
        x = random.uniform(a, b)       
        y = random.uniform(c, d)
        s += funcao(x, y)
    media = s/n
    return media*(b-a)*(d-c)

if __name__ == "__main__":
    n = 1000             
    '''é possível colocar um número muito alto aqui para comparar a velocidade das funções,
    no entanto, ter um número enorme de divisões não é prático, pois ainda que o usuário necessite de uma precisão enorme,
    o número obtido pela integral de simpson apenas com n= 1000 tem um erro de 6,8*10e-15,
    sendo que um número floating point do python não consegue representar um número muito menor que esse, então,
    nesse ponto, a precisão não pode ficar maior.'''
    
    print(integral_trap(math.sin, 0, math.pi, n*3))         #n*3
    print(integral_rect(math.sin, 0, math.pi, n)*6)         #n*6
    print(integral_simpson(math.sin, 0, math.pi, n*2))      #n*2, as quantidades aqui são multiplicadas por 3, 6 e 2 para cancelar a diferença de velocidade entre elas, assim é possível comparar a precisão obtida por cada método depois de um mesmo período de tempo
    f = lambda x, y: math.sin(x)*math.cos(y)
    print(monteCarlo(0, math.pi/2, 0, math.pi/2, f, n))
