import numpy as np
import matplotlib.pyplot as plt
from typing import List
from utils import InterpBase


class Linear_Interp(InterpBase):
    def __init__(self, x, y):
        super().__init__(x, y)

    def __call__(self, x_desejado):
        if isinstance(x_desejado, (int, float)):
            return self._linear_interp_single(x_desejado)
        else:
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