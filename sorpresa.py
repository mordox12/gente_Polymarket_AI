import turtle
import colorsys

# --- CONFIGURACIÓN DE LA PANTALLA ---
# Esto crea la ventana donde dibujaremos
screen = turtle.Screen()
screen.setup(width=1000, height=800)
screen.bgcolor('black') # Fondo negro para que los colores neón resalten mucho más
screen.title("¡El Pez Neón para mi Primo!")

# --- CONFIGURACIÓN DE LA TORTUGA ---
# Nuestra "pluma" mágica
t = turtle.Turtle()
t.speed(0) # ¡Máxima velocidad! Para que no se aburra esperando
t.width(3) # Líneas gruesas para que se vean bien
t.hideturtle() # Escondemos la flecha para que solo se vea el dibujo

# --- FUNCIÓN MÁGICA DE COLORES ---
# Usamos el sistema HSV para crear un arcoíris que cambia suavemente
def obtener_color(paso, total_pasos):
    # Genera un tono (hue) diferente en cada paso
    hue = paso / total_pasos
    # Convierte HSV (Tono, Saturación, Brillo) a RGB para Turtle
    color = colorsys.hsv_to_rgb(hue, 1, 1) # Saturación y brillo al máximo para neón
    return color

# --- PARÁMETROS DEL DIBUJO ---
num_escamas = 160  # Cuántas líneas forman el pez (más = más detallado, pero más lento)
largo_inicial = 5  # Tamaño inicial
angulo = 119       # El ángulo mágico que crea la forma de pez al girar
t.penup()
t.goto(-150, 0)   # Empezamos un poco a la izquierda
t.pendown()

# --- ¡A DIBUJAR EL PEZ NEÓN! ---
print("¡Empezando el dibujo! Mira cómo se crea la magia...")

# Un bucle principal que dibuja cada "pétalo" o línea
for i in range(num_escamas):
    # 1. Cambiar color
    t.color(obtener_color(i, num_escamas))
    
    # 2. Moverse hacia adelante (el tamaño crece un poquito cada vez)
    t.forward(largo_inicial + i * 1.65)
    
    # 3. Girar
    # Este giro crea el efecto de espiral que forma el cuerpo y las aletas
    t.left(angulo)
    
    # 4. Dibujar una pequeña "curva" al final de cada línea para las escamas
    # Esto le da la textura que se ve en la imagen original
    if i % 2 == 0:
        t.circle(i/4, 40)
    else:
        t.circle(-i/4, 40)

# --- DETALLE FINAL: EL OJO ---
# Un pez necesita un ojo
t.penup()
t.goto(-220, 100) # Lo posicionamos donde iría el ojo
t.pendown()
t.color('white')
t.begin_fill()
t.circle(20) # Círculo exterior blanco
t.end_fill()

t.penup()
t.goto(-210, 115)
t.pendown()
t.color('black')
t.begin_fill()
t.circle(10) # Pupila negra
t.end_fill()

# --- MENSAJE PARA TU PRIMO ---
t.penup()
t.goto(-350, -350)
t.color('white')
t.write("¡HECHO CON CÓDIGO!", font=("Arial", 30, "bold italic"))

# Esto mantiene la ventana abierta al terminar
print("¡Dibujo terminado! Pulsa en la ventana para salir.")
screen.exitonclick()