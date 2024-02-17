import array
import unittest

class Matrix:
    """
    Clase que representa una matriz.
    """

    def __init__(self, rows, cols, elements=None):
        self.rows = rows
        self.cols = cols
        self.elements = array.array('i', [0] * (rows * cols)) if elements is None else array.array('i', [element for row in elements for element in row])

    def __str__(self):
        return '\n'.join(['   '.join(map(str, self.elements[i:i+self.cols])) for i in range(0, len(self.elements), self.cols)])

    def __getitem__(self, index):
        i, j = index
        return self.elements[i * self.cols + j]

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Las matrices deben tener las mismas dimensiones para la suma.")
        result = Matrix(self.rows, self.cols)
        result.elements = array.array('i', [a + b for a, b in zip(self.elements, other.elements)])
        return result

    def __mul__(self, scalar):
        result = Matrix(self.rows, self.cols)
        result.elements = array.array('i', [element * scalar for element in self.elements])
        return result

    def tolist(self):
        return [self.elements[i:i + self.cols].tolist() for i in range(0, len(self.elements), self.cols)]


    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda.")
        result = Matrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                result.elements[i * result.cols + j] = sum(self.elements[i * self.cols + k] * other.elements[k * other.cols + j] for k in range(self.cols))
        return result

    def cambiar_renglones(self, i, j):
        """
        Cambia dos renglones de la matriz.

        Args:
        - i, j: índices de los renglones que se intercambiarán.
        """
        temp = array.array('i', self.elements[j * self.cols: j * self.cols + self.cols])
        for k in range(self.cols):
            self.elements[j * self.cols + k] = self.elements[i * self.cols + k]
            self.elements[i * self.cols + k] = temp[k]

    def multiplicar_renglon(self, i, escalar):
        """
        Multiplica un renglón de la matriz por un escalar.

        Args:
        - i: índice del renglón que se multiplicará.
        - escalar: el escalar por el cual se multiplicará el renglón.
        """
        for k in range(i * self.cols, i * self.cols + self.cols):
            self.elements[k] *= escalar

    def sumar_renglones(self, i, j, escalar=1):
        """
        Suma un múltiplo de un renglón a otro renglón.

        Args:
        - i, j: índices de los renglones que se sumarán.
        - escalar: el escalar por el cual se multiplicará el renglón i antes de sumarlo.
        """
        for k in range(self.cols):
            self.elements[i * self.cols + k] += self.elements[j * self.cols + k] * escalar


class TestMatrixMethods(unittest.TestCase):
    def test_matrix_initialization(self):
        matrix = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(matrix.rows, 2)
        self.assertEqual(matrix.cols, 3)
        self.assertEqual(matrix.tolist(), [[1, 2, 3], [4, 5, 6]])

    def test_matrix_addition(self):
        matrix_a = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        matrix_b = Matrix(2, 3, [[7, 8, 9], [10, 11, 12]])
        result = matrix_a + matrix_b
        self.assertEqual(result.tolist(), [[8, 10, 12], [14, 16, 18]])

    def test_scalar_multiplication(self):
        matrix = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        result = matrix * 2
        self.assertEqual(result.tolist(), [[2, 4, 6], [8, 10, 12]])

    def test_matrix_multiplication(self):
        matrix_a = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        matrix_b = Matrix(3, 2, [[7, 8], [9, 10], [11, 12]])
        result = matrix_a.multiply(matrix_b)
        self.assertEqual(result.tolist(), [[58, 64], [139, 154]])

    def test_cambiar_renglones(self):
        matrix = Matrix(3, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix.cambiar_renglones(0, 2)
        self.assertEqual(matrix.tolist(), [[7, 8, 9], [4, 5, 6], [1, 2, 3]])

    def test_multiplicar_renglon(self):
        matrix = Matrix(3, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix.multiplicar_renglon(1, 2)
        self.assertEqual(matrix.tolist(), [[1, 2, 3], [8, 10, 12], [7, 8, 9]])

    def test_sumar_renglones(self):
        matrix = Matrix(3, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix.sumar_renglones(0, 2, 2)
        self.assertEqual(matrix.tolist(), [[15, 18, 21], [4, 5, 6], [7, 8, 9]])


if __name__ == '__main__':
    unittest.main()
