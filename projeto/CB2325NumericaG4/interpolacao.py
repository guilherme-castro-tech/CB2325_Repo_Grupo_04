import numpy as np
import math
import matplotlib.pyplot as plt
from typing import List
from .utils import InterpBase

class Poly_Interp(InterpBase):
    '''
      Classe que cria um polinômio interpolador pelo método de Newton, 
      retornando o gráfico e, quando definida e chamada com um argumento,
      retorna o valor do polinômio no x dado.

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
      self.calcular_coef()

    def calcular_coef(self):
      """
      Esta função calcula os coeficientes do polinômio interpolador
      utilizando o método de Newton (diferenças divididas) e atualizando
      o objeto da classe 'self.coeficientes'.
      """
      tabela = np.zeros((self.n, self.n))
      tabela[:,0] = self.y

      for j in range(1, self.n):
          for i in range(self.n - j):
              numerador = tabela[i+1, j-1] - tabela[i, j-1]
              denominador = self.x[i+j] - self.x[i]
              if denominador == 0:
                  raise ZeroDivisionError('Há dois pontos com a mesma coordenada x.')
              tabela[i, j] = numerador / denominador
      self.coeficientes = tabela[0,:]

    def __call__(self, x_desejado):
        """
        Esta função permite a classe ser chamada como o
        polinômio interpolador, retornando seu valor no
        x desejado.

        Parâmetros:
        x_desejado (float, int ou list): Coordenada(s) x('s) que
        queremos avaliar.

        Retorna: Um Array com os valores do polinômio interpolador.

        """
        # Transforma a entrada em Numpy Array
        x_desejado = np.atleast_1d(x_desejado)

        def func_valor(x_val):
          """
          Esta função calcula o valor do polinômio interpolador
          para um dado x pelo método de Horner.

          Parâmetros:
          x_val (float): coordenada x.

          Retorna: Um float com o valor de x no polinômio interpolador.

          """
          resultado = self.coeficientes[self.n - 1]
          for i in range(self.n - 2, -1, -1):
              resultado = self.coeficientes[i] + (x_val - self.x[i]) * resultado
          return resultado

        valores = np.array([func_valor(x_val) for x_val in x_desejado])

        # Se for somente um ponto, passa o Array para um float ou int
        if isinstance(x_desejado, (int, float)):
            return valores.item()
        return valores


    def erro(self, func_original, pontos):
        """
        Esta função calcula o erro absoluto entre o polinômio atual e uma 
        função verdadeira em uma lista de pontos de teste.

        Parâmetros:
        func_original (function): Função original com a qual queremos comparar;
        pontos (int, float ou list): Ponto(s) para calculo de erro.

        Retorna: Um Array com o(s) erro(s).

        """
        lista_pontos = np.atleast_1d(pontos)
        errors = []
        for p in pontos:
            erros_val = np.abs(self(p) - func_original(p))
            errors.append(erros_val)
        return np.array(errors).flatten()


    def __repr__(self):
        '''
        Retorna a representação do objeto
        de Interpolação bem como os coeficientes do polinômio.
        '''
        return f'Poly_Interp(Grau={self.n-1}) \n\tx={self.x}, \n\ty={self.y} \n\tCoeficientes={self.coeficientes})'
    

    def grafico(self):
        ''' a partir de INterpBase.grafico(), cria um gráfico com o polinômio interpolador e os pontos dados.
        
        Returns:
            Mostra o gráfico do polinômio e os pontos de interpolação.
        '''
        return super().grafico()

    

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
           return  np.nan                       ## A maneira de tratar extrapolação aqui é retornar NaN.

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
        return super().grafico()

class Hermite_Interp(InterpBase):

    '''
    Classe que cria um polinômio interpolador de Hermite a partir dos pontos dados, 
    retornando o gráfico e quando definida e chamada com um argumento, retorna o valor do 
    polinômio no valor do argumento.
    '''

    def __init__(self, x_points:list, y_points:list, dy_points:list):

        '''
        Args:
            x_points: lista que representa as coordenadas x's dos pontos.
            y_points: lista que representa as coordenadas y's dos pontos.
            dy_points: lista que representa as derivadas nos pontos x's.
        Return:
            Quando somente inicializada, retorna: 
            calcular_coef(): retorna uma lista com os coeficientes encontrados. 
            grafico(): retorna um gráfico do polinômio interpolador e os pontos dados. 
        '''
        
        super().__init__(x_points, y_points)
        self.dy = np.array(dy_points)
        if self.n != len(dy_points):
            raise TypeError('x, y e dy não possuem o mesmo tamanho')
        self.coeficientes = None
        self.tabela = None 
        self.calcular_coef()
        
    def calcular_coef(self):

        ''' Calcula os coeficientes do polinômio interpolador de Hermite usando 
        diferenças divididas.

        A tabela de diferenças divididas é construída considerando que cada ponto x_i é repetido duas vezes para acomodar 
        tanto o valor da função quanto o valor da derivada.   

        Return:
            Atualiza self.coeficientes com os coeficientes do polinômio de Hermite.
        '''

        self.tabela = np.zeros((2*self.n, 2*self.n))

        for i in range(self.n):
            self.tabela[2*i, 0] = self.y[i]
            self.tabela[2*i + 1, 0] = self.y[i]
            self.tabela[2*i, 1] = self.dy[i] 

            print(self.tabela)
            
            if i < self.n - 1:
                #diferença dividida do método de Newton para pontos distintos
                self.tabela[2*i + 1, 1] = (self.y[i+1] - self.y[i]) / (self.x[i+1] - self.x[i])
            else:
                self.tabela[2*i + 1, 1] = self.dy[i]  

        #adiciona os números na tabela
        for j in range(2, 2*self.n):
            for i in range(2*self.n - j):
                numerador = self.tabela[i + 1, j - 1] - self.tabela[i, j - 1]
                denominador = self.x[(i + j) // 2] - self.x[i // 2]  
                if denominador == 0:
                    # Para pontos duplicados, usa a derivada
                    self.tabela[i, j] = self.dy[i // 2] / math.factorial(j)
                else:
                    self.tabela[i, j] = numerador / denominador
                    
        
        # a primeira linha da tabela contém os coeficientes do polinômio
        self.coeficientes = self.tabela[0, :]

    def valor_polinomio(self, x_desejado):

        ''' Avalia o polinômio interpolador de Hermite no ponto x_desejado.
        Args:
            x_desejado: valor ou array de valores onde o polinômio deve ser avaliado.
        Return:
            Valor do polinômio no(s) ponto(s) x_desejado.
        '''


        x_desejado = np.atleast_1d(x_desejado)

        def evaluate_single_point(x_val):

            ''' Avalia o polinômio em um único ponto x_val. 
             Args:
                x_val: valor onde o polinômio deve ser avaliado.
             Return:
                Valor do polinômio no ponto x_val.
            '''
            
            resultado = self.coeficientes[0]
            produto = 1.0
            
            for i in range(1, 2*self.n):
                produto *= (x_val - self.x[(i-1) // 2])  
                resultado += self.coeficientes[i] * produto
            
            return resultado

        return np.array([evaluate_single_point(x_val) for x_val in x_desejado])
    
    
    def __call__(self, x_desejado):
        """
        Avalia o polinômio com verificação de extrapolação.
        Retorna None para pontos fora do intervalo [min(x), max(x)].
        """
        # Verifica se é extrapolação
        if np.isscalar(x_desejado):
            # Para um único valor
            if x_desejado < np.min(self.x) or x_desejado > np.max(self.x):
                return None
        else:
            # Para arrays/listas
            x_desejado = np.asarray(x_desejado)
            if np.any(x_desejado < np.min(self.x)) or np.any(x_desejado > np.max(self.x)):
                # Se algum ponto estiver fora, retorna None
                return None
        
        # Se não é extrapolação, calcula normalmente
        return self.valor_polinomio(x_desejado)
        
    def grafico(self, salvar_como = None):

        """
        Cria um gráfico com a interpolação linear e os pontos dados.
        """
        return super().grafico()


if __name__ == "__main__":
    x_points = [1, 2, 3]
    y_points = [1, 4, 9]

    #interpolação polinomial
    print("\n--- Testando Poly_Interp ---")
    interp_poly = Poly_Interp(x_points, y_points)

    print(f"Coeficientes do polinômio (b_0, b_1, ...): {interp_poly.coeficientes}")
    # Testando o polinômio
    print(f"Valor do polinômio em x=1: {interp_poly(1)}")
    print(f"Valor do polinômio em x=2: {interp_poly(2)}")
    print(f"Valor do polinômio em x=3: {interp_poly(3)}")
    print(f"Valor do polinômio em x=2.3: {interp_poly(2.5)}")
    print(interp_poly.grafico())
    print(f"Valor em x=2.0: {interp_poly(2.0)}")
    #interp = interp_poly()

    #interpolação linear
        
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

    #interpolação de hermite
    
    print("\n--- Testando HermiteInterpolator ---")
    x_hermite = [1, 2, 3]
    y_hermite = [1, 8, 27]
    dy_hermite = [3, 6, 9]  # Deriv
    interp_hermite = Hermite_Interp(x_hermite, y_hermite, dy_hermite)
    print(f"Coeficientes do polinômio (b_0, b_1, ...): {interp_hermite.coeficientes}")
    # Testando o polinômio
    print(f"Valor do polinômio em x=1: {interp_hermite(1)}")
    print(f"Valor do polinômio em x=2: {interp_hermite(2)}")
    print(f"Valor do polinômio em x=3: {interp_hermite(3)}")
    print(f"Valor do polinômio em x=2.5: {interp_hermite(2.5)}")
    interp_hermite.grafico()
        
