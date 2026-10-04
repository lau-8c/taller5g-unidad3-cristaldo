# ejercicio2_roseta.py
# Generador de rosetas geometricas con el algoritmo de Bresenham
from PIL import Image
import math
import colorsys


# Función Bresenham 
def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Bresenham generalizado, aritmetica entera exclusivamente."""
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


# Puntos equiespaciados
def generar_puntos_circulo(cx, cy, radio, n):
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        puntos.append((x, y))
    return puntos


#  Color del gradiente según el ángulo y la distancia al centro 
def color_gradiente(x0, y0, x1, y1, cx, cy, radio):
    # Punto medio de la línea
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    # Ángulo del punto medio respecto al centro 
    angulo = math.atan2(my - cy, mx - cx)
    tono = (angulo + math.pi) / (2 * math.pi)  # normalizado entre 0 y 1
    # Distancia del punto medio al centro -> define el brillo
    distancia = math.hypot(mx - cx, my - cy) / radio  # entre 0 y 1
    valor = 0.55 + 0.45 * min(distancia, 1.0)
    r, g, b = colorsys.hsv_to_rgb(tono, 1.0, valor)
    return (int(r * 255), int(g * 255), int(b * 255))


# Dibuja todas las líneas entre pares de puntos
def dibujar_roseta(pixels, puntos, ancho, alto):
    n = len(puntos)
    cx, cy = ancho // 2, alto // 2
    radio = 300
    for i in range(n):
        for j in range(i + 1, n):  
            x0, y0 = puntos[i]
            x1, y1 = puntos[j]
            color = color_gradiente(x0, y0, x1, y1, cx, cy, radio)
            bresenham(pixels, x0, y0, x1, y1, color, ancho, alto)

# Programa principal: tres variantes

for n in [12, 24, 36]:
    img = Image.new("RGB", (700, 700), "white")
    pixels = img.load()
    puntos = generar_puntos_circulo(350, 350, 300, n)
    dibujar_roseta(pixels, puntos, 700, 700)
    img.save(f"roseta_{n}.png")
    if n == 24:
        img.save("roseta.png")  # salida base pedida en el enunciado
    print(f"Generada roseta_{n}.png ({n * (n - 1) // 2} líneas)")