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


