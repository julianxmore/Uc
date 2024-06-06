import time
import busio
import board
import displayio
import adafruit_displayio_ssd1306
from adafruit_ov7670 import OV7670, OV7670_SIZE_DIV16, OV7670_COLOR_YUV

# Configuración de I2C para la pantalla OLED
displayio.release_displays()
i2c = busio.I2C(board.GP27, board.GP26)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

# Configuración de la cámara OV7670
cam_bus = busio.I2C(board.GP21, board.GP20)
cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP8,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP9,
    shutdown=board.GP15,
    reset=board.GP14,
)
cam.size = OV7670_SIZE_DIV16
cam.colorspace = OV7670_COLOR_YUV
cam.flip_y = True

# Tamaño del búfer de imagen
buf = bytearray(2 * cam.width * cam.height)

# Configuración de UART
uart = busio.UART(board.GP16, board.GP17, baudrate=19200)

# Define el umbral para distinguir negro de blanco
umbral = 128  # Puedes ajustar este valor según sea necesario

def capture_and_display():
    cam.capture(buf)
    
    # Crear un bitmap para la pantalla OLED
    bitmap = displayio.Bitmap(128, 32, 2)  # Pantalla de 128x32 con 2 colores
    palette = displayio.Palette(2)
    palette[0] = 0x000000  # Negro
    palette[1] = 0xFFFFFF  # Blanco

    # Centrar y redimensionar la imagen capturada en la OLED
    cam_width = cam.width
    cam_height = cam.height
    oled_width = 128
    oled_height = 32

    # Tomar la región central de la cámara (40x30)
    start_x = (cam_width - oled_width // 3) // 2
    start_y = (cam_height - oled_height // 3) // 2

    for j in range(oled_height // 3):
        for i in range(oled_width // 3):
            # Invertir el orden de los píxeles en la dirección horizontal
            inverted_i = (oled_width // 3 - 1) - i
            # Obtiene el byte de intensidad de luz de la región central de la imagen
            intensity = buf[2 * (cam_width * (start_y + j) + (start_x + inverted_i))]
            # Establece el color en el bitmap
            color = 1 if intensity > umbral else 0
            for dx in range(3):
                for dy in range(3):
                    if (3 * i + dx) < 128 and (3 * j + dy) < 32:
                        bitmap[3 * i + dx, 3 * j + dy] = color

    # Crear un TileGrid y mostrarlo en la pantalla
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
    display_group = displayio.Group()
    display_group.append(tile_grid)
    display.show(display_group)

    # Lista para almacenar el último renglón de la visualización como binario
    last_row_binary = []
    for i in range(cam.width):
        if cam.height > 29:  # Asegurarse de que estamos en el último renglón capturado
            intensity = buf[2 * (cam.width * 15 + i)]
            last_row_binary.append('0' if intensity > umbral else '1')

    # Convierte la lista binaria a una cadena de texto
    data = "".join(last_row_binary)
    
    # Envía la bandera de inicio seguida de los datos por UART
    uart.write(data.encode())
    print(data)
# Capturar y mostrar imágenes en un bucle infinito
while True:
    capture_and_display()
    # Esperar un momento antes de la siguiente captura
 # Esperar un momento antes de la siguiente captura
