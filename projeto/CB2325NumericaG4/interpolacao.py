def liner_interp(xp_data:list,yp_data:list, x_est:list):
    '''
    Essa função gera uma interpolação linear por partes
    para um conjunto discreto de pontos, obedecendo à
    seguinte fórmula y = y_0 + [(y_1-y_0)/(x_1-x_0)].(x-x_0)

    Ou seja, o ponto (x,y) é obtido encontrando o valor 
    correspondente da ordenada y dados um ponto abscissa x
    tal que este estaja no seguinto de reta que liga o ponto
    (x_0,y_0) ao ponto (x_1,y_1)

    Args:
        xp_data (list) : lista ordenada dos pontos da abscissa 
        yp_data (list) : lista ordenada dos pontos da ordenada
        x_est   (list) : lista ordenada dos pontos que se deseja estimar a função
    Returns:
        y_est (list) : lista dos pontos associados ao x_est
    '''

    if len(xp_data) != len(yp_data):
        raise IndexError("As listas xp_data e yp_data não têm mesmo tamanho!")
    if len(xp_data) < 2:
        raise IndexError("Pelo menos dois pontos necessários para interpolar!")
    
    y_est = []                                          # Lista para guardar valores estimados 
    for x in x_est:
        '''
        3 casos:
        - menor que o menor ponto
        - maior que o maior ponto
        - entre os pontos
        '''
        if x < xp_data[0]:                              # menor que o menor ponto
            x0 , y0 = xp_data[0], yp_data[0]
            x1 , y1 = xp_data[1], yp_data[1] 
        
        elif x > xp_data[-1]:                           # maior que o maior ponto
            x0 , y0 = xp_data[-2], yp_data[-2]
            x1 , y1 = xp_data[-1], yp_data[-1] 

        else:
            for i in range(len(xp_data)-1):             ## Iterando sobre a lista ordenada x, associada a y para encontrar em que segmento de rete estão os pontos
                if (xp_data[i]<x) and (x<=xp_data[i+1]):## Aqui eu assumi que está entre os pontos, mas se ele estiver exatamente no ponto?
                    x0, y0 = xp_data[i], yp_data[i]
                    x1, y1 = xp_data[i+1], yp_data[i+1]
                    break
                if xp_data[i] == x:                     ## Assumindo que ele é um dos pontos do meu conjunto de pontos
                    x0, y0 = xp_data[i], yp_data[i]
                    x1, y1 = xp_data[i+1], yp_data[i+1] ## y0 = y(x0) para não quebrar boas práticas, definimos isso    
                
        y = y0 + [(y1-y0)/(x1-x0)]*(x-x0)               ## Calcular o valor de x e adicionar à lista de y_est
        y_est.append(y)

    return y_est

import matplotlib.pyplot as plt
import numpy as np
### BASE DO CÓDIGO, QUE AINDA SERÁ UNIDO COM OS DEMAIS DE INTERPOLAÇÃO E RECEBERÁ COMENTÁRIOS E DOCSTRINGS
class poly_interp:
    ''' 
      Classe que cria um polinômio interpolador a partir dos pontos dados pelo método de Newton, 
      retornando o gráfico e quando definida e chamada com um argumento, retorna o valor do 
      polinômio no valor do argumento.

      Args:
          x: lista que representa as coordenadas x's dos pontos.
          y: lista que representa as coordenadas y's dos pontos.
      
      Return:
          Quando somente inicializada, retorna:
          calcular_coef(): retorna uma lista com os coeficientes encontrados. 
          grafico(): retorna um gráfico do polinômio interpolador e os pontos dados. 
    '''

    def __init__(self,x:list,y:list):
      self.n = len(x)
      if self.n != len(y):
        raise TypeError('x e y não possuem o mesmo tamanho')
      self.x = np.array(x)
      self.y = np.array(y)
      self.coeficientes = None
      self.tabela = None
      self.calcular_coef()
      self.grafico()

    def calcular_coef(self):
      self.tabela = np.zeros((self.n, self.n))
      self.tabela[:,0] = self.y
      for j in range(1, self.n):
        for i in range(self.n - j):
          numerador = self.tabela[i+1, j-1] - self.tabela[i, j-1]
          denominador = self.x[i+j] - self.x[i]
          if denominador == 0:
            raise ZeroDivisionError('Há dois pontos com a mesma coordenada x.')
          self.tabela[i, j] = numerador / denominador
      self.coeficientes = self.tabela[0,:]

    def valor_polinomio(self, x_desejado):
      x_desejado = np.atleast_1d(x_desejado)
      def evaluate_single_point(x_val):
        resultado = self.coeficientes[self.n - 1]
        for i in range(self.n - 2, -1, -1):
          resultado = self.coeficientes[i] + (x_val - self.x[i]) * resultado
        return resultado
      return np.array([evaluate_single_point(x_val) for x_val in x_desejado])

    def __call__(self, x_desejado):
      return self.valor_polinomio(x_desejado)

    ##### Gráfico provisório 
    def grafico(self):
      curva_x = np.linspace(min(self.x), max(self.x), 200)
      y_polinomio = self.valor_polinomio(curva_x)
      fig, ax1 = plt.subplots(figsize=(10, 6))
      fig.suptitle(f'Interpolação de Newton (Grau {self.n-1})')

      ax1.plot(curva_x, y_polinomio, color='blue', linestyle='-', label=f'Polinômio $P_{{{self.n-1}}}(x)$ (Newton)')
      ax1.scatter(self.x, self.y, color='red', marker='o', zorder=5, label='Pontos de Interpolação')
      ax1.set_xlabel('Eixo X')
      ax1.set_ylabel('Valor de $P(x)$', color='blue')
      ax1.tick_params(axis='y', labelcolor='blue')
      ax1.grid(True)
      ax1.legend(loc='upper left')
      plt.show()

x_points = [1, 2, 3]
y_points = [1, 4, 9]

interpolator = poly_interp(x_points, y_points)
print(f"Coeficientes do polinômio (b_0, b_1, ...): {interpolator.coeficientes}")

# Testando o polinômio
print(f"Valor do polinômio em x=1: {interpolator(1)}")
print(f"Valor do polinômio em x=2: {interpolator(2)}")
print(f"Valor do polinômio em x=3: {interpolator(4)}")
print(f"Valor do polinômio em x=2.5: {interpolator(2.5)}")

