import matplotlib.pyplot as plt
import numpy as np
### BASE DO CÓDIGO, QUE AINDA SERÁ UNIDO COM OS DEMAIS DE INTERPOLAÇÃO E RECEBERÁ COMENTÁRIOS E DOCSTRINGS

class Poly_Interp():
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

    def __init__(self, x:list, y:list):
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
        if isinstance(x_desejado, int) or isinstance(x_desejado, float) or len(x_desejado) == 1:
          return self.valor_polinomio(x_desejado)
        else:
          return np.array([self.valor_polinomio(x) for x in x_desejado])

    ##### Gráfico provisório 
    def grafico(self, salvar_como = None):
      curva_x = np.linspace(min(self.x), max(self.x), 200)
      fig, ax1 = plt.subplots(figsize=(10, 6))
      ax1.set_xlabel('Eixo X')
      ax1.set_ylabel('Valor de Interpolação', color='blue')
      ax1.tick_params(axis='y', labelcolor='blue')
      ax1.grid(True)

      y_interp = self.valor_polinomio(curva_x)
      title = f'Interpolação de Newton (Grau {self.n-1})'
      plot_label = f'Polinômio $P_{{{self.n-1}}}(x)$ (Newton)'
      
      fig.suptitle(title)
      ax1.plot(curva_x, y_interp, color='blue', linestyle='-', label=plot_label)
      ax1.scatter(self.x, self.y, color='red', marker='o', zorder=5, label='Pontos de Interpolação')
      ax1.legend(loc='upper left')
      
      if salvar_como:
            try:
                plt.savefig(salvar_como)
                print(f"Gráfico salvo em: {salvar_como}")
            except Exception as e:
                print(f"Erro ao salvar o gráfico: {e}")
      plt.show()

    def __repr__(self):
      '''
      Retorna a representação do objeto
      de Interpolação bem como o polinômio
      interpolador dos pontos.
      '''
      polinomio = f"P(x) = {self.coeficientes[0]:.3f}"
      for i in range(1, self.n):
        term =f" + {self.coeficientes[i]:.3f}" if self.coeficientes[i] >= 0 else f" - {abs(self.coeficientes[i]):.3f}"
        product_str = ""
        for j in range(i):
          x_val = self.x[j]
          if x_val == 0:
            product_str += "(x)"
          else:
            sign = "-" if x_val > 0 else "+"
            product_str += f"(x {sign} {abs(x_val)})"
          polinomio+= term+product_str
      repr = f'Interp(metodo = Polinomial) \n\tx={self.x}, \n\ty={self.y} \n\t{polinomio})'
      return repr
      


class Linear_Interp():
    def __init__(self, x, y):
       self.x = x 
       self.y = y
       self.grafico()
      

    def __call__(self,  x_desejado):
        if isinstance(x_desejado, int) or isinstance(x_desejado, float) or len(x_desejado) == 1:
          return self._liner_interp(x_desejado)
        else:
           return np.array([self._liner_interp(x) for x in x_desejado])

    def __repr__(self):
      repr = f'Interp(metodo = linear \n\tx={self.x}, \n\ty={self.y})'
      return repr
    
    def _liner_interp(self, x_est):          ## Método privado, acessado pelo argumento ao chamar a classe:
      '''
      Essa função gera uma interpolação linear por partes
      para um conjunto discreto de pontos, obedecendo à
      seguinte fórmula y = y_0 + [(y_1-y_0)/(x_1-x_0)].(x-x_0)

      Ou seja, o ponto (x,y) é obtido encontrando o valor 
      correspondente da ordenada y dados um ponto abscissa x
      tal que este estaja no seguinto de reta que liga o ponto
      (x_0,y_0) ao ponto (x_1,y_1)

      Args:
          self.x (np.array) : lista ordenada dos pontos da abscissa 
          self.y (np.array) : lista ordenada dos pontos da ordenada
          x_est  (float) ou (int) : ponto a estimar
      Returns:
          y_est (float) ou (int) : ponto estimado
      '''
      if x_est<self.x[0] or x_est > self.x[-1]:
         return None                        ## A maneira de tratar extrapolação aqui é retornar None.
      
      for i in range(len(self.x)- 1):
         if self.x[i] <= x_est <= self.x[i+1]:
            x0,y0 = self.x[i], self.y[i]
            x1,y1 = self.x[i+1], self.y[i+1]

            if x1 == x0: 
              y_est = y0
              return y_est
            
            tg_theta = (y1-y0)/(x1-x0)
            y_est = y0 + tg_theta * (x_est - x0)
            return y_est
          # Caso x_est seja exatamente o último ponto
      if x_est == self.x[-1]:
        return self.y[-1]
         
      return None
    
    def grafico(self, salvar_como = None):

      curva_x = np.linspace(min(self.x), max(self.x), max(1000,10*len(self.x)))
      fig, ax1 = plt.subplots(figsize=(10, 6))
      ax1.set_xlabel('Eixo X')
      ax1.set_ylabel('Valor de Interpolação', color='blue')
      ax1.tick_params(axis='y', labelcolor='blue')
      ax1.grid(True)

      y_interp = np.array([self._liner_interp(x)for x in curva_x])
      title = f'Interpolação Linear'
      plot_label = f''

      fig.suptitle(title)
      ax1.plot(curva_x, y_interp, color='blue', linestyle='-', label=plot_label)
      ax1.scatter(self.x, self.y, color='red', marker='o', zorder=5, label='Pontos de Interpolação')
      ax1.legend(loc='upper left')
      
      if salvar_como:
            try:
                plt.savefig(salvar_como)
                print(f"Gráfico salvo em: {salvar_como}")
            except Exception as e:
                print(f"Erro ao salvar o gráfico: {e}")
      plt.show()
    
if __name__ == "__main__":

  x_points = [1, 2, 3]
  y_points = [1, 4, 9]

  interpolator = Poly_Interp(x_points, y_points)
  print(f"Coeficientes do polinômio (b_0, b_1, ...): {interpolator.coeficientes}")
  # Testando o polinômio
  print(f"Valor do polinômio em x=1: {interpolator(1)}")
  print(f"Valor do polinômio em x=2: {interpolator(2)}")
  print(f"Valor do polinômio em x=3: {interpolator(3)}")
  print(f"Valor do polinômio em x=2.3: {interpolator(2.5)}")

  interpolator2 = Linear_Interp(x_points, y_points)
  # Testando Interpolação Linear
  print(f"Valor de interpolação linear em x=1: {interpolator2(1)}")
  print(f"Valor de interpolação linear em x=2: {interpolator2(2)}")
  print(f"Valor de interpolação linear em x=3: {interpolator2(3)}")
  print(f"Valor de interpolação linear em x=2.3: {interpolator2(2.5)}")

  # interpolator.grafico(salvar_como="CB2325_Repo_Grupo_04/images/interp_newton.png")
  # interpolator2.grafico(salvar_como="CB2325_Repo_Grupo_04/images/interp_linear.png")

  print(interpolator)