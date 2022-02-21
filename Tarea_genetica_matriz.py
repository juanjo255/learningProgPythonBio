def cambio_base(decimal, base):
    # Esta variable va a guardar los residuos de cada division
    # Para formar el codigo
    conversion = '' 

    # Ciclo para repetir la divisiones con el cociente del anterior
    # Y guardar el residuo de cada division
    while decimal // base != 0:
        residuo = decimal % base
        conversion = str (residuo) + conversion
        decimal = decimal // base
        
    # se suma el ultimo cociente antes del 0 que seria 1
    # Pues el residuo de cero sera 1
    return str(decimal) + conversion

def matriz_alelos (numero_genes, numero_alelos):

    # Almacenamos las combinaciones posibles
    combinaciones_posibles = numero_alelos ** numero_genes

    # Matriz inicial
    import numpy as np
    matrix = np.zeros (shape = (combinaciones_posibles, combinaciones_posibles))

    # Lista con las combinaciones de los estados de los genes
    combinaciones = list ()

    # formamos las combinaciones posibles para 2 estados
    # aprovechando el comportamiento binario
    for i in range (combinaciones_posibles):
        i = cambio_base (i, numero_alelos)
        if len (i) < numero_genes:
            i = "0" * (numero_genes - len (i)) + i
        combinaciones.insert (0, i)

    # Combinamos los estados y llenamos la matriz
    for fila in range (len (combinaciones)):
        valor = sum (int (i) for i in combinaciones [fila])
        for columna in range (len (combinaciones)):
            matrix [fila] [columna] = valor + sum (int (i) for i in combinaciones [columna])
            
    print (matrix)

numero_genes = int (input ("Ingresa el numero de genes a combinar: "))
numero_alelos = int (input ("Ingresa el numero de alelos a combinar: "))
matriz_alelos (numero_genes, numero_alelos)
