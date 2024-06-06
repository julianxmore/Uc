import network
import socket
from machine import Pin, PWM, UART
import utime
import time
import _thread
import array
import random



# Crear instancia de UART
uart = UART(0, baudrate=19200, tx=Pin(0), rx=Pin(1))

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
def detener_motores():
    in1_motor1.value(0)
    in2_motor1.value(0)
    in1_motor2.value(0)
    in2_motor2.value(0)
    pwm_motor1.duty_u16(0)
    pwm_motor2.duty_u16(0)# Mantener la velocidad del motor 2 constante  # Mantener la velocidad del motor 2 constante

def recibir_datos_uart():
    ultima_lista_valida = None  # Variable para mantener la última lista con al menos un '1'

    while True:
        try:
            # Leer datos UART
            data_received = uart.read(1000)  # Lee una cadena de hasta 1000 bytes
            
            if data_received:
                try:
                    data_list = data_received.decode().strip()  # Eliminar espacios en blanco
                
                except UnicodeError:
                    continue
                direction = "forward"
                count_left = 0
                count_front = 0
                count_right = 0

                # Contar los unos en cada sección
                for i, value in enumerate(data_list[-40:]):
                    if value == '1':
                        if i < 10:
                            count_left += 1
                        elif 10 <= i < 30:
                            count_front += 1
                        else:
                            count_right += 1

                
                #print(f"Left count: {count_left}, Front count: {count_front}, Right count: {count_right}")

                # Si hay al menos un '1' en la lista, actualizar la última lista válida
                if '1' in data_list:
                    ultima_lista_valida = data_list

                # Determinar la dirección en función del conteo de unos
                if count_front > count_left and count_front > count_right:
                    direction = "forward"
                elif count_left > count_front and count_left > count_right:
                    direction = "left"
                elif count_right > count_left and count_right > count_front:
                    direction = "right"
                elif count_left == 0 and count_front == 0 and count_right == 0:
                    #print(ultima_lista_valida)
                    if ultima_lista_valida:
                        for i, value in enumerate(ultima_lista_valida[-40:]):
                            if value == '1':
                                if i < 20:
                                    direction = "left"
                                else: 
                                    direction = "right"
                                break
                    
                    
                if direction in ["left", "right"]:
                    control_motor(direction)
                    time.sleep(0.15)
                    control_motor("stop")
                else:
                    control_motor(direction)
                    

                
                
        except KeyboardInterrupt:
            break

recibir_datos_uart()

