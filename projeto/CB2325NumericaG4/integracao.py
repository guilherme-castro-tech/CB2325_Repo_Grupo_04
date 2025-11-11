import math
import pytest
import math, random

def integral_trap(funcao, a, b, n=10):        #integração por trapézios
    """O primeiro parametro é uma função, O segundo e o 
    Terceiro são os limites de integração, O
     Quarto é em quantos trapezios você que aproximar a sua função"""

    dx = (b-a)/n#Comprimento do intervalo
    s = 0
    for c in range(n):
        s += (funcao(a + c*dx) + funcao(a + (c+1)*dx))*(dx/2) #Calcula as aproximações
    return s


def integral_rect(funcao, a, b, n=10):            #essa função usa uma sequência parecida com a do método de trapézios
    """
    O primeiro parâmetro é uma função, o segundo e o 
    terceiro são os limites de integração, o quarto é
    em quantos retângulos a função é dividida.
    """
    dx = (b-a)/n    
    s = 0
    #lista = [i for i in range(n)]

    for c in range(n):
        s += (funcao(a + c*dx))*dx
    return s

def integral_simpson(funcao, a, b, n=10):
    """O primeiro parametro é uma função, O segundo e o 
    Terceiro são os limites de integração, O
    Quarto é em quantos trapezios você quer aproximar a sua função"""

    dx = (b-a)/n    #Comprimento do intervalo
    s = 0
    for c in range(n):
        s += (funcao(a + c*dx) + 4 * funcao((a + a + c * dx + (c+1) * dx)/2) + funcao(a + (c+1)*dx))*(dx/6)         #Calcula as aproximações
    return s
    
def monteCarlo(a, b, c, d, funcao, n=10):
    """monte Carlo é magia"""
    """
    Para calcular Integrais de funções de 2 variaveis, 
    ou seja, Calcular volume, podemos escolher n pontos no R² de forma aleatória, 
    calcular o valor da função nesses pontos, somar todos. 
    Após isso, fazer uma média de todos os valores e multiplicar pela área do domínio"""
    s = 0
    for i in range(n):
        x = random.uniform(a, b)        #Escolhe a coordenada 
        y = random.uniform(c, d)
        s += funcao(x, y)
    
    media = s/n
    return media*(b-a)*(d-c)

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

if __name__ == "__main__":
    n = 1000             
    '''é possível colocar um número muito alto aqui para comparar a velocidade das funções,
    no entanto, ter um número enorme de divisões não é prático, pois ainda que o usuário necessite de uma precisão enorme,
    o número obtido pela integral de simpson apenas com n= 1000 tem um erro de 6,8*10e-15,
    sendo que um número floating point do python não consegue representar um número muito menor que esse, então,
    nesse ponto, a precisão não pode ficar maior.'''
    
    print(integral_trap(math.sin, 0, math.pi, n*3))         #n*3
    print(integral_rect(math.sin, 0, math.pi, n)*6)         #n*6
    print(integral_simpson(math.sin, 0, math.pi, n*2))#n*2, as quantidades aqui são multiplicadas por 3, 6 e 2 para cancelar a diferença de velocidade entre elas, assim é possível comparar a precisão obtida por cada método depois de um mesmo período de tempo
    #print(integral_rect(math.sin, 0, math.pi, n))
    f = lambda x, y: math.sin(x)*math.cos(y)
    print(monteCarlo(0, math.pi/2, 0, math.pi/2, f, n))
    
    pytest.main(["-v", __file__])


