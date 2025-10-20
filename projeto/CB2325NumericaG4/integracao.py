import math




def integral(funcao, a, b, n):
    """O primeiro parametro é uma função, O segundo e o 
    Terceiro são os limites de integração, O
     Quarto é em quantos trapezios você que aproximar a sua função"""

    dx = (b-a)/n#Comprimento do intervalo
    s = 0
    for c in range(n):
        s += (funcao(a + c*dx) + funcao(a + (c+1)*dx))*(dx/2) #Calcula as aproximações
    return s


if __name__ == "__main__":
    print(integral(math.sin, 0, math.pi, 100))


