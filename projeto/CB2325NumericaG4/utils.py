import numpy as np
import matplotlib.pyplot as plt
from typing import List

class Domain:
    min = None
    max = None

    def __contains__(self):
        raise NotImplementedError
    
    def __repr__(self):
        raise NotImplementedError
    
    def __str__(self):
        return self.__repr__()
    
    def copy(self):
        raise NotImplementedError
    
class Interval(Domain):
    def __init__(self,p1,p2):
        self.inff = min(p1,p2)
        self.supp = max(p1,p2)

    @property
    def min(self):
        return self.inff
    
    @property
    def max(self):
        return self.supp
    
    @property
    def size(self):
        return (self.max - self.min)
    
    @property
    def half(self):
        return(self.max-self.min)/2
    
    def __contains__(self,x):
        return np.all(np.logical_and(self.inff<=x, x<= self.supp))
    
    def __str__(self):
        return super().__str__()
    
    def __repr__(self):
        return super().__repr__()
    
    def copy(self):
        return Interval(self.inff,self.supp)
    

class RealFunction:
    f = None
    prime = None
    domain = None

    def eval_safe(self,x):
        if self.domain is None or x in self.domain:
            try:
                return self.f(x)
            except (ValueError, TypeError):
                return np.nan # Lida com casos onde f(x) não pode ser calculado
        else:
            return np.nan # Retorna NaN para extrapolação
        
    def prime_safe(self,x):
        if self.domain is None or x in self.domain:
            try:
                return self.prime(x)
            except (ValueError, TypeError):
                return np.nan
        else:
            return np.nan ## Retonando NaN no mesmo caso do de cima
        
    def __call__(self, x) -> float:
        return self.eval_safe(x)
    
    def plot(self):
        fig, ax = plt.subplots()
        X = np.linspace(self.domain.min,self.domain.max,500)
        Y = self(X)
        ax.plot(X,Y)
        return fig, ax
    
class InterpBase(RealFunction):
    """
    Classe base abstrata para métodos de interpolação. Interpolação é uma RealFunction em um domínio [x_i,x_f]
    """
    
    def __init__(self, x:List[float], y: List[float]):
        if len(x) != len(y):
            raise TypeError("Ambos os conjuntos devem possuir mesma cardinalidade (tamanho)")
        
        idx_sorted = np.argsort(x)
        self.x = np.array(x)[idx_sorted]
        self.y = np.array(y)[idx_sorted]
        self.n = len(self.x)

        self.domain = Interval(self.x[0], self.x[-1])        
        self.f = self.__call__
        self.prime = None

    def __call__(self, x_desejado):
        raise NotImplementedError("A classe filha implementa a __call__")

    def plot_nodes(self):
        fig, ax = self.plot()

        ax.scatter(self.x, self.y, color = "red", zorder=5, label = 'Pontos de Interpolação')
        ax.legend()
        plt.show()

        

