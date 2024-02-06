from array import array

def cambiar_renglones(matriz, i, j):
    """
    Función para cambiar dos renglones de una matriz.

    Args:
    - matriz: matriz representada como un arreglo de 9 elementos.
    - i, j: índices de los renglones que se intercambiarán.

    Returns:
    - matriz: la matriz después de cambiar los renglones.
    """
    matriz = matriz[:]
    temp = array('f', matriz[j*3:j*3+3])
    for k in range(3):
        matriz[j*3+k] = matriz[i*3+k]
        matriz[i*3+k] = temp[k]
    return matriz

def multiplicar_renglon(matriz, i, escalar):
    """
    Función para multiplicar un renglón de la matriz por un escalar.

    Args:
    - matriz: matriz representada como un arreglo de 9 elementos.
    - i: índice del renglón que se multiplicará.
    - escalar: el escalar por el cual se multiplicará el renglón.

    Returns:
    - matriz: la matriz después de la multiplicación.
    """
    matriz = matriz[:]
    for k in range(i*3, i*3+3):
        matriz[k] *= escalar
    return matriz

def sumar_renglones(matriz, i, j, escalar=1):
    """
    Función para sumar un múltiplo de un renglón a otro renglón.

    Args:
    - matriz: matriz representada como un arreglo de 9 elementos.
    - i, j: índices de los renglones que se sumarán.
    - escalar: el escalar por el cual se multiplicará el renglón i antes de sumarlo.

    Returns:
    - matriz: la matriz después de la suma.
    """
    matriz = matriz[:]
    for k in range(3):
        matriz[i*3+k] += matriz[j*3+k] * escalar
    return matriz

# Arreglo dado
h = array('f', [1.1, 2.2, 3.3,
                4.4, 5.5, 6.6,
                7.7, float('-inf'), float('nan')])

# Ejemplo de uso
# Cambiar el renglón 0 con el renglón 1
h1 = cambiar_renglones(h, 0, 1)
print("Matriz después de cambiar renglones 0 y 1:")
print(h1)
print()

# Multiplicar el renglón 2 por 1/3
h2 = multiplicar_renglon(h, 2, 1/3)
print("Matriz después de multiplicar el renglón 2 por 1/3:")
print(h2)
print()

# Sumar el renglón 1 al renglón 0
h3 = sumar_renglones(h, 0, 1)
print("Matriz después de sumar el renglón 1 al renglón 0:")
print(h3)
