import network
import socket
from machine import Pin, PWM, UART
import utime
import time
import _thread
import array
import random

class Matrix:
    def __init__(self, m, n, data=None):
        self.m = m  # number of rows
        self.n = n  # number of columns
        if data is None:
            self.data = array.array('f', [0.0] * (n * m))
        else:
            if len(data) != n * m:
                raise ValueError("Incorrect data length")
            self.data = array.array('f', data)

    def __getitem__(self, index):
        if isinstance(index,tuple):
            i, j = index
            if isinstance(i,int) and isinstance(j,int):
                if 0 <= i < self.m and 0 <= j < self.n:
                    return self.data[i * self.n + j]
                else:
                    raise IndexError("Matrix indices out of range")
            if isinstance(i,int) and isinstance(j,slice):
                raise IndexError("One slice is not allowed yet ")
            if isinstance(i,slice) and isinstance(j,int):
                raise IndexError("One slice is not allowed yet ")
            if isinstance(i,slice) and isinstance(j,slice):
                start_i, stop_i, step_i = i.indices(self.m)
                start_j, stop_j, step_j = j.indices(self.n)
                sliced_data = [self.data[r * self.n + c] for r in range(start_i, stop_i, step_i) for c in range(start_j, stop_j, step_j)]
                return Matrix(stop_i - start_i, stop_j - start_j, sliced_data)
            else:
                raise IndexError("i,j indices are required")
        else:
            raise ValueError("i,j indices are required")

    def __setitem__(self, index, value):
        i, j = index
        if 0 <= i < self.m and 0 <= j < self.n:
            self.data[i * self.n + j] = value
        else:
            raise IndexError("Matrix indices out of range")

    def __add__(self, other):
        if isinstance(other, Matrix) and self.n == other.n and self.m == other.m:
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] + other[i, j]
            return result
        else:
            raise ValueError("Matrices of different dimensions cannot be added")

    def __sub__(self, other):
        if isinstance(other, Matrix) and self.n == other.n and self.m == other.m:
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] - other[i, j]
            return result
        else:
            raise ValueError("Matrices of different dimensions cannot be subtracted")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            result = Matrix(self.m, self.n)
            for i in range(self.m):
                for j in range(self.n):
                    result[i, j] = self[i, j] * other
            return result
        elif isinstance(other, Matrix):
            if self.n != other.m:
                raise ValueError("Number of columns of first matrix must be equal to number of rows of second matrix")
            result = Matrix(self.m, other.n)
            for i in range(self.m):
                for j in range(other.n):
                    for k in range(self.n):
                        result[i, j] += self[i, k] * other[k, j]
            return result
        else:
            raise ValueError("Multiplication not defined for these data types")

    def T(self):
        transposed_data = array.array('f', [0.0] * (self.n * self.m))
        for i in range(self.m):
            for j in range(self.n):
                transposed_data[j * self.m + i] = self.data[i * self.n + j]
        return Matrix(self.n, self.m, transposed_data)

    def __or__(self,other):
        if isinstance(other, Matrix) and self.n == other.n :
            return Matrix(self.m + other.m, self.n,self.data+other.data)
        else:
            raise ValueError("Matrices of different dimensions cannot be added")

    def __and__(self, other):
        if self.m != other.m:
            raise ValueError("Matrices must have the same number of rows to concatenate horizontally")
        
        concatenated_data = []
        for i in range(self.m):
            concatenated_data.extend(self.data[i*self.n : (i+1)*self.n])
            concatenated_data.extend(other.data[i*other.n : (i+1)*other.n])

        return Matrix(self.m, self.n + other.n, concatenated_data)

    def __str__(self):
        output = ""
        for i in range(self.m):
            row_str = " ".join(str(self[i, j]) for j in range(self.n))
            output += row_str + "\n"
        return output

class Perceptron:
    def __init__(self, input_size, output_size):
        self.weights = Matrix(input_size, output_size,  [random.random() for _ in range(input_size * output_size)])  
        self.bias = Matrix(1,output_size, [random.random() for _ in range(output_size)])  

    def predict(self, inputs):
        result = inputs * self.weights  + self.bias
        return result

    def train(self, inputs, labels, learning_rate=0.1, epochs=1):
        for epoch in range(epochs):
            predictions = self.predict(inputs)
            error = labels - predictions
            self.weights += inputs.T() * error * learning_rate
            self.bias += error * learning_rate
            return error
        
    def save_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"{self.weights.m} {self.weights.n}\n")
            for i in range(self.weights.m):
                for j in range(self.weights.n):
                    file.write(str(self.weights[i, j]) + ' ')
                file.write('\n')
            for j in range(self.bias.n):
                file.write(str(self.bias[0, j]) + ' ')
            file.write('\n')

    @classmethod
    def load_file(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            rows, cols = map(int, file.readline().split())
            weights_data = []
            for _ in range(rows):
                row = list(map(float, file.readline().split()))
                weights_data.extend(row)
            weights = Matrix(rows, cols, weights_data)
            bias_data = list(map(float, file.readline().split()))
            bias = Matrix(1, cols, bias_data)
            perceptron = cls(rows, cols)
            perceptron.weights = weights
            perceptron.bias = bias
            return perceptron
        
perceptron = Perceptron.load_file('perceptron_training.txt')
def mean_squared_error(valores_reales, valores_predichos):
    # Verificamos que las dos matrices tengan las mismas dimensiones
    if valores_reales.m != valores_predichos.m or valores_reales.n != valores_predichos.n:
        raise ValueError("Las matrices deben tener las mismas dimensiones")
    
    # Inicializamos la suma de los cuadrados de las diferencias
    suma_cuadrados_diferencias = 0.0
    
    # Calculamos la suma de los cuadrados de las diferencias
    for i in range(valores_reales.m):
        for j in range(valores_reales.n):
            diferencia = valores_reales[i, j] - valores_predichos[i, j]
            suma_cuadrados_diferencias += diferencia ** 2
    
    # Calculamos el error cuadrático medio dividiendo la suma total por el número de elementos
    error_cuadratico_medio = suma_cuadrados_diferencias / (valores_reales.m * valores_reales.n)
    
    return error_cuadratico_medio

          
class Reinforcement:
  def __init__(self,n_in, n_out, list_outs,f_error):
    """
    n_in, n_out : number of inputs and outputs
    list_outs : a Matrix of spected outputs. each row is one output
    f_error : input -> realnumber that represents the error of that input

    """
    self.n_in = n_in
    self.n_out = n_out
    self.list_outs = list_outs
    self.f_error = f_error
    self.control = Perceptron( n_in, n_out)
    self.model = Perceptron(n_in + n_out, n_in)
    self.input_old =None
    self.output_old =None



  def predict(self, input_):

    output =self.control.predict(input_)
    
    if self.input_old is not None and self.output_old is not None:
         self.train(self.input_old, self.output_old, input_, output)
        
    self.input_old=input_
    self.output_old=output
    return output
     
  
  def train(self , input_old ,  output_old , input_ , output):
      self.model.train(input_old & output_old,input_)
      out_selected=None
      min_error=float('inf')
      for out_i in self.list_outs:
          in_predic = self.model.predict(input_ & out_i)
          error_pred = self.f_error(input_, in_predic)
          if (error_pred < min_error) or (None == min_error):
              min_error = error_pred
              out_selected= out_i
      self.control.train(input_,out_selected)        

     


uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
direcciones = {
    "forward": Matrix(1, 3, [ 0, 0, 1]),
    "left": Matrix(1, 3, [ 0, 1, 0]),
    "rigth": Matrix(1, 3, [ 1, 0, 0])
    
}
reinforcement = Reinforcement(40, 3, list(direcciones.values()), mean_squared_error)
# Configurar pines del puente H y PWM para motores
in1_motor1 = Pin(8, Pin.OUT)
in2_motor1 = Pin(9, Pin.OUT)

# Configurar los pines del puente H para el segundo motor
in1_motor2 = Pin(13, Pin.OUT)
in2_motor2 = Pin(12, Pin.OUT)

# Configurar los pines PWM para controlar la velocidad de los motores
pwm_motor1 = PWM(Pin(2))  # Pin 2 como PWM para el primer motor
pwm_motor2 = PWM(Pin(4))  # Pin 3 como PWM para el segundo motor

# Configuración de velocidad
normal_speed = 1000  # Velocidad normal en términos de duty cycle de 16 bits
turning_speed = 300  # Velocidad de giro reducida
def control_motor(direction):
    # Envía la dirección por UART
   

    if direction == "forward":
        in1_motor1.value(0)
        in2_motor1.value(1)
        in1_motor2.value(0)
        in2_motor2.value(1)
    elif direction == "backward":
        in1_motor1.value(1)
        in2_motor1.value(0)
        in1_motor2.value(1)
        in2_motor2.value(0)
    elif direction == "left":
        in1_motor1.value(0)
        in2_motor1.value(1)
        in1_motor2.value(0)
        in2_motor2.value(1)
    elif direction == "right":
        in1_motor1.value(0)
        in2_motor1.value(1)
        in1_motor2.value(0)
        in2_motor2.value(1)
    else:
        # Detener ambos motores si no se especifica una dirección válida
        in1_motor1.value(0)
        in2_motor1.value(0)
        in1_motor2.value(0)
        in2_motor2.value(0)


 # Ajustar la velocidad según la dirección
    if direction == "left":
        # Configuración para girar a la izquierda
        pwm_motor1.freq(2000)  # Frecuencia PWM de 1000 Hz para el motor 1
        pwm_motor1.duty_u16(int(0.4*65535)) # Reducir la velocidad del motor 1
        pwm_motor2.freq(5500)  #Frecuencia PWM de 1000 Hz para el motor 2
        pwm_motor2.duty_u16(int(0.93*65535))   # Mantener la velocidad del motor 2 constante
    elif direction == "right":
        # Configuración para girar a la derecha
        pwm_motor1.freq(5500)  # Frecuencia PWM de 1000 Hz para el motor 1
        pwm_motor1.duty_u16(int(0.95*65535))  # Mantener la velocidad del motor 1 constante
        pwm_motor2.freq(3000)  # Frecuencia PWM de 1000 Hz para el motor 2
        pwm_motor2.duty_u16(int(0.4*65535))  # Reducir la velocidad del motor 2
    elif direction == "backward":
        # Configuración para detener ambos motores
       pwm_motor1.freq(2000)  # Frecuencia PWM de 5000 Hz para el motor 1
       pwm_motor1.duty_u16(int(0.7*65535))  # Máxima velocidad del motor 1
       pwm_motor2.freq(1000)  # Frecuencia PWM de 5000 Hz para el motor 2
       pwm_motor2.duty_u16(int(0.7*65535))  # Reducir la velocidad del motor 2
    else:
        # Configuración para otras direcciones (forward, 
       pwm_motor1.freq(10000)  # Frecuencia PWM de 5000 Hz para el motor 1
       pwm_motor1.duty_u16(int(0.88*65535))  # Máxima velocidad del motor 1
       pwm_motor2.freq(10000)  # Frecuencia PWM de 5000 Hz para el motor 2
       pwm_motor2.duty_u16(int(0.83*65535))
    

def recibir_datos_uart():
    # Mantener la velocidad del motor 2 constante  # Mantener la velocidad del motor 2 constantedef recibir_datos_uart():
    while True:
        try:
            data_list = []  # Limpia data_list en cada iteración

            data_received = uart.read(1000)  # Lee una cadena de hasta 1000 bytes

            if data_received:
                data_list = []
                try:
                    data_list = list(data_received.decode().strip())
                
                    
                except UnicodeError:
                    continue
                input_data = Matrix(1, 40, [int(x) for x in data_list[-40:]])
                
                
                prediction = reinforcement.predict(input_data)
                
    

                # Obtener el índice del valor máximo en la matriz de salida
                max_value = max(prediction.data)
                max_index = None
                for i in range(len(prediction.data)):
                    if prediction.data[i] == max_value:
                        max_index = i
                        break

    
                direction = list(direcciones.keys())[max_index]
                print(direction)
    
                if direction in ["left", "right"]:
                    control_motor(direction)
                    time.sleep(0.15)
                    control_motor("stop")
                else:
                    control_motor(direction)


                #print(error)
                #perceptron.save_file('perceptron_training.txt')

        except KeyboardInterrupt:
            break


recibir_datos_uart()




          
