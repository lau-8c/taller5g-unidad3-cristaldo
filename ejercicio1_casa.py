# ejercicio1_casa.py
# Composicion geometrica de una casa usando el algoritmo DDA
from PIL import Image
import math


# Función DDA 
def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una linea usando el algoritmo DDA."""
    dx, dy = x1 - x0, y1 - y0
    pasos = max(abs(dx), abs(dy))
    if pasos == 0:
        return
    x_inc, y_inc = dx / pasos, dy / pasos
    x, y = x0, y0
    for _ in range(int(pasos) + 1):
        px, py = round(x), round(y)
        if 0 <= px < ancho and 0 <= py < alto:
            pixels[px, py] = color
        x += x_inc
        y += y_inc


#  Rectangulos
def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)  
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)  
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)  
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)  


# Triangulos
def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


# Puerta: un rectangulo con su propio color 
def dibujar_puerta(pixels, x0, y0, x1, y1, color, ancho, alto):
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)


# Ventana: un rectángulo (cuadrado) con su propio color 
def dibujar_ventana(pixels, x0, y0, lado, color, ancho, alto):
    dibujar_rectangulo(pixels, x0, y0, x0 + lado, y0 + lado, color, ancho, alto)


# Sol: rayos que irradian desde un punto central 
def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        dda(pixels, cx, cy, x, y, color, ancho, alto)


# Linea de piso que cruza toda la imagen 
def dibujar_piso(pixels, y, color, ancho, alto):
    dda(pixels, 0, y, ancho - 1, y, color, ancho, alto)


# Programa principal
ancho, alto = 600, 500
imagen = Image.new("RGB", (ancho, alto), (200, 230, 255))  
pixels = imagen.load()

# Colores 
COLOR_CUERPO = (139, 69, 19)     # marrón
COLOR_TECHO = (200, 30, 30)      # rojo
COLOR_PUERTA = (30, 60, 180)     # azul
COLOR_VENTANAS = (0, 150, 150)   # turquesa
COLOR_SOL = (255, 170, 0)        # naranja/amarillo
COLOR_PISO = (0, 140, 0)         # verde

# Piso (y = 400)
dibujar_piso(pixels, 400, COLOR_PISO, ancho, alto)

# Cuerpo de la casa
dibujar_rectangulo(pixels, 150, 250, 400, 400, COLOR_CUERPO, ancho, alto)

# Techo (triángulo sobre el cuerpo)
dibujar_triangulo(pixels, (130, 250), (275, 150), (420, 250), COLOR_TECHO, ancho, alto)

# Puerta (centro de la casa)
dibujar_puerta(pixels, 250, 320, 300, 400, COLOR_PUERTA, ancho, alto)

# Dos ventanas cuadradas
dibujar_ventana(pixels, 175, 280, 50, COLOR_VENTANAS, ancho, alto)
dibujar_ventana(pixels, 325, 280, 50, COLOR_VENTANAS, ancho, alto)

# Sol en la esquina superior derecha (12 rayos)
dibujar_sol(pixels, 520, 70, 50, 12, COLOR_SOL, ancho, alto)

# Guardar resultado
imagen.save("casa.png")
print("Imagen generada: casa.png")