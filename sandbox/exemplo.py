import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd())))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

import numpy as np
from projeto.CB2325NumericaG4.integracao import plot_integral_simpson
from projeto.CB2325NumericaG4.aproximacao import plot_regressao

plot_integral_simpson(np.sin, 3, 6)
pontos = [(1, 2), (2, -2), (3, 5), (4, 7)]
plot_regressao(pontos=pontos, grau=2)