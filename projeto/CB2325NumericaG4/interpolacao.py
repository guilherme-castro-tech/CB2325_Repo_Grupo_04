import numpy as np
import matplotlib.pyplot as plt
from typing import List
from utils import InterpBase

class Poly_Interp(InterpBase):
    '''
      Classe que cria um polinômio interpolador a partir de nós de Chebyshev pelo
      método de Newton, retornando o gráfico e, quando definida e chamada com um
      argumento, retorna o valor do polinômio no x dado.

      Args:
          x: lista que representa as coordenadas x's dos pontos.
          y: lista que representa as coordenadas y's dos pontos.

      Return:
          Quando somente inicializada, retorna:
          calcular_coef(): retorna uma lista com os coeficientes encontrados.
          grafico(): retorna um gráfico do polinômio interpolador e os pontos dados.
    '''

    def __init__(self, x:list, y:list):
      super().__init__(x, y) 
      
      self.coeficientes = None
      self.tabela = None
      self.calcular_coef()

    def calcular_coef(self):
        """
        Calcula os coeficientes do polinômio interpolador pelo
        método de Newton.

        Args:
          None.

        Returns:
            np.array: Retorna os coeficientes em ordem crescente.
        """
        self.tabela = np.zeros((self.n, self.n))
        self.tabela[:,0] = self.y # Usa self.y_nodes da classe base

        for j in range(1, self.n):
            for i in range(self.n - j):
                numerador = self.tabela[i+1, j-1] - self.tabela[i, j-1]
                denominador = self.x[i+j] - self.x[i] # Usa self.x_nodes
                if denominador == 0:
                    raise ZeroDivisionError('Há dois pontos com a mesma coordenada x.')
                self.tabela[i, j] = numerador / denominador
        self.coeficientes = self.tabela[0,:]

    def __call__(self, x_desejado):
        """
        Permite a classe ser chamada como uma função, retornando
        o valor do polinômio interpolador no x desejado.

        Args:
          x_desejado: Pode ser somente um ponto ou um Array de
          pontos.

        Returns:
            float: Caso a entrada seja um só ponto.
            np.array: Caso a entrada seja um Array.
        """
        x_desejado = np.atleast_1d(x_desejado)
        
        def func_valor(x_val):
            resultado = self.coeficientes[self.n - 1]
            for i in range(self.n - 2, -1, -1):
                resultado = self.coeficientes[i] + (x_val - self.x[i]) * resultado
            return resultado
        
        valores = np.array([func_valor(x_val) for x_val in x_desejado])
        
        if isinstance(x_desejado, (int, float)):
            return valores.item()
        return valores
    
    def nos_de_chebyshev(self):
        """
        Calcula os nós de Chebyshev do primeiro tipo no intervalo
        dos pontos x's dados à classe.

        Args:
          None.

        Returns:
            nos: Um array dos nós de Chebyshev no intervalo.
        """
        k = np.arange(self.n)
        x_cheb= np.cos((2 * k + 1) * np.pi / (2 * self.n))
        nos = ((self.x[-1] - self.x[0]) / 2) * x_cheb + (self.x[0]+self.x[-1])/2
        return nos

    def erro(self, true_function, test_points: list) -> np.ndarray:
        """
        Calcula o erro absoluto entre o polinômio atual e uma função verdadeira
        em uma lista de pontos de teste.

        Args:
            true_function (callable): A função verdadeira para comparação.
            test_points (list): Uma lista de pontos onde o erro será calculado.

        Returns:
            np.ndarray: Um array contendo os erros absolutos em cada ponto de teste.
        """
        test_points = np.atleast_1d(test_points)
        errors = []
        for p in test_points:
            error_val = np.abs(self(p) - true_function(p))
            errors.append(error_val)
        return np.array(errors).flatten()

    def grafico(self, salvar_como = None):
        """
        Cria um gráfico com o polinômio interpolador e os pontos dados.

        Args:
          salvar_como: diretório em que o gráfico deverá ser salvo.
        Returns:
            gráfico.
        """
        curva_x = np.linspace(self.domain.min, self.domain.max, max(500, 10 * self.n))
        y_interp = self(curva_x)

        fig, ax = self.plot()

        fig.suptitle('Interpolação Polinomial')
        ax.plot(curva_x, y_interp, color='blue', linestyle='-', label='Interpolação Polinomial por Newton')
        ax.scatter(self.x, self.y, color='red', marker='o', zorder=5, label='Pontos de Interpolação')
        ax.legend(loc='upper left')
        if salvar_como:
                try:
                    fig.savefig(salvar_como)
                    print(f"Gráfico salvo em: {salvar_como}")
                except Exception as e:
                    print(f"Erro ao salvar o gráfico: {e}")
        plt.show()

    def __repr__(self):
        '''
        Retorna a representação do objeto
        de Interpolação bem como os coeficientes do polinômio.
        '''
        # Simplificando a representação para evitar complexidade na geração do polinômio em string
        return f'Poly_Interp(Grau={self.n-1}) \n\tx={self.x}, \n\ty={self.y} \n\tCoeficientes={self.coeficientes})'

class Linear_Interp(InterpBase):
    def __init__(self, x, y):
        super().__init__(x, y)

    def __call__(self, x_desejado):
        if np.isscalar(x_desejado):
            return self._linear_interp_single(x_desejado)
        return np.array([self._linear_interp_single(x) for x in x_desejado])
    
    def _linear_interp_single(self, x_est):
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
        """
        Cria um gráfico com a interpolação linear e os pontos dados.
        """
        curva_x = np.linspace(self.domain.min, self.domain.max, max(500, 10 * self.n))
        
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.set_xlabel('Eixo X')
        ax1.set_ylabel('Valor de Interpolação', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.grid(True)

        y_interp = self(curva_x)
        
        fig.suptitle('Interpolação Linear por Partes')
        ax1.plot(curva_x, y_interp, color='blue', linestyle='-', label='Interpolação Linear')
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

  print("\n--- Testando Poly_Interp ---")
  interp_poly = Poly_Interp(x_points, y_points)

  print(f"Coeficientes do polinômio (b_0, b_1, ...): {interp_poly.coeficientes}")
  # Testando o polinômio
  print(f"Valor do polinômio em x=1: {interp_poly(1)}")
  print(f"Valor do polinômio em x=2: {interp_poly(2)}")
  print(f"Valor do polinômio em x=3: {interp_poly(3)}")
  print(f"Valor do polinômio em x=2.3: {interp_poly(2.5)}")
  print(interp_poly)
  print(f"Valor em x=2.0: {interp_poly(2.0)}")
  interp_poly.grafico()

    
  x_linear = [0, 1, 3, 4, 6]
  y_linear = [0, 2, 1, 5, 4]

  interp_linear = Linear_Interp(x_linear, y_linear)

  print(interp_linear)

  print(f"\nValor em x=0: {interp_linear(0)}")                          # Deve ser 0  (Testa interpolação em pontos conhecidos) 
  print(f"Valor em x=3: {interp_linear(3)}")                            # Deve ser 1
  print(f"Valor em x=6: {interp_linear(6)}")                            # Deve ser 4

  print(f"\nValor em x=0.5: {interp_linear(0.5)}")                      # Pontos Intermediários
  print(f"Valor em x=2.0: {interp_linear(2.0)}") 
  print(f"Valor em x=5.0: {interp_linear(5.0)}") 

  pontos_teste = np.array([0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 6.0])          # Valores intermediários
  valores_teste = interp_linear(pontos_teste)
  print(f"\nValores para \n{pontos_teste}: \n{valores_teste}")

  print(f"\nValor em x=-1.0 (extrapolação): {interp_linear(-1.0)}")     # Testa extrapolação
  print(f"Valor em x=7.0 (extrapolação): {interp_linear(7.0)}")

  interp_linear.grafico() ## Testa gráfico
