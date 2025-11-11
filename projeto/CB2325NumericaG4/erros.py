import numpy as np

def erro_relativo(true_f, aprox_f):
    '''
    Calcula erro relativo de uma função
    erro_rel = |true_f - aprox_f|/true_f
    '''
    return (erro_absoluto(true_f,aprox_f)/true_f)

def erro_absoluto(true_f, aprox_f):
    '''
    Calcula erro absoluto de uma função
    erro_abs = |true_f - apox_f|
    '''
    return np.abs(true_f - aprox_f)