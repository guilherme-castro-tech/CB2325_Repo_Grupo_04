import math




def integral_trap(funcao, a, b, n):        #integração por trapézios
    """O primeiro parametro é uma função, O segundo e o 
    Terceiro são os limites de integração, O
     Quarto é em quantos trapezios você que aproximar a sua função"""

    dx = (b-a)/n#Comprimento do intervalo
    s = 0
    for c in range(n):
        s += (funcao(a + c*dx) + funcao(a + (c+1)*dx))*(dx/2) #Calcula as aproximações
    return s

import numpy as np
def integral_rect(funcao, a, b, n):            #integração por retângulos. Estou tentando encontrar uma forma mais rápida de fazer a integração. 
                                               #Esse método usa um array e aplica a função por meio de map ao invés de aplicar em um valor de cada vez com o 'for', é um pouco mais rápido, mas ocupa muita memória. Não consegui contornar esse problema ainda.
    """
    O primeiro parâmetro é uma função, o segundo e o 
    terceiro são os limites de integração, o quarto é
    em quantos retângulos a função é dividida.
    """
    s = 0
    dx = (b-a)/ n
    chunk = n // 10000
    vals = a + dx*np.arange(n)
    lista = map(funcao, vals)
    s = sum(lista)*dx
    #print(chunk)
    '''for start in range(0,n,chunk):
        end = min(n,chunk+start)
        vals = a + (dx*np.arange(start,end))
        arr = np.fromiter(map(funcao,vals),dtype=float)
        s += float(np.sum(arr)*dx)'''
    return s

def integral_rect2(funcao, a, b, n):            #essa função usa uma sequência parecida com a do método de trapézios
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

if __name__ == "__main__":
    n = 100000000
    print(integral_trap(math.sin, 0, math.pi, n))
    print(integral_rect(math.sin, 0, math.pi, n))
    print(integral_rect(math.sin, 0, math.pi, n))
