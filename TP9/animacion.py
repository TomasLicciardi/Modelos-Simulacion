import pygame
import sys
import random
import os
import cv2

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Animación de Figuras')

# Colores
BACKGROUND_COLOR = (30, 30, 30)
PRIMARY_COLOR = (70, 130, 180)
SECONDARY_COLOR = (220, 20, 60)
TEXT_COLOR = (255, 255, 255)

# Función para centrar la figura principal y el círculo secundario
def center_figure_and_circle(fig_type, fig_width, fig_height):
    if fig_type == 'cuadrado' or fig_type == 'rectangulo':
        fig_x = (width - fig_width) // 2
        fig_y = (height - fig_height) // 2
        circle_x = fig_x + fig_width // 2
        circle_y = fig_y + fig_height // 2
    elif fig_type == 'circulo':
        dimension = max(fig_width, fig_height)
        fig_x = (width - dimension) // 2
        fig_y = (height - dimension) // 2
        circle_x = fig_x + dimension // 2
        circle_y = fig_y + dimension // 2
    return fig_x, fig_y, circle_x, circle_y

# Solicitar al usuario el tamaño de los cuadrados
while True:
    try:
        user_size = int(input("Ingrese el tamaño de los cuadrados (entre 1 y 10): "))
        if 1 <= user_size <= 10:
            user_size /= 5
            break
        else:
            print("Por favor, ingrese un número entre 1 y 10.")
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número entre 1 y 10.")

# Solicitar la figura principal
while True:
    figura = input("Ingrese la figura principal (cuadrado, rectangulo o circulo): ")
    if figura in ['cuadrado', 'rectangulo', 'circulo']:
        break
    else:
        print("Entrada no válida. Por favor, ingrese una figura válida.")

# Solicitar dimensiones de la figura entre 1 y 1000:
if figura == 'cuadrado':
    dimension = int(input("Ingrese el tamaño de un lado del cuadrado (1-1000 mm): "))
    dimension = max(100, min(600, dimension))
    fig_x, fig_y, circle_x, circle_y = center_figure_and_circle('cuadrado', dimension, dimension)
    width = height = dimension
elif figura == 'rectangulo':
    width = int(input("Ingrese el ancho del rectángulo (1-1000 mm): "))
    height = int(input("Ingrese el largo del rectángulo (1-1000 mm): "))
    width = max(100, min(600, width))
    height = max(100, min(600, height))
    fig_x, fig_y, circle_x, circle_y = center_figure_and_circle('rectangulo', width, height)
elif figura == 'circulo':
    dimension = int(input("Ingrese el diámetro del círculo (1-1000 mm): "))
    dimension = max(100, min(600, dimension))
    fig_x, fig_y, circle_x, circle_y = center_figure_and_circle('circulo', dimension, dimension)
    width = height = dimension

# Dimensiones del círculo secundario (1/4 del tamaño de la figura principal)
circle_diameter = min(width, height) // 4
circle_radius = circle_diameter // 2

# Lista para almacenar los cuadrados generados
# Cada cuadrado será representado como [x, y, side_length, direction, stopped]
cuadrados = []

# Tiempo de control para generar cuadrados cada segundo (ajustar para simulación rápida)
last_time = pygame.time.get_ticks()
interval = 200  # 200 ms para acelerar la simulación

# Variables para rastrear el tiempo y la cantidad de cuadrados generados
start_ticks = pygame.time.get_ticks()
cuadrados_generados = 0

# Función para verificar si un cuadrado toca el borde de la figura principal
def check_collision_with_figure(x, y, size):
    if (x <= fig_x or x + size >= fig_x + width or 
        y <= fig_y or y + size >= fig_y + height):
        return True
    return False

# Función para verificar si un cuadrado toca otro cuadrado que ya está detenido
def check_collision_with_stopped_squares(x, y, size):
    for square in cuadrados:
        if square[4]:  # Solo chequea los cuadrados detenidos
            other_x, other_y, other_size = square[0], square[1], square[2]
            if (x < other_x + other_size and
                x + size > other_x and
                y < other_y + other_size and
                y + size > other_y):
                return True
    return False

# Función para verificar si un cuadrado detenido toca el círculo rojo
def check_collision_with_red_circle(x, y, size):
    square_center_x = x + size // 2
    square_center_y = y + size // 2
    distance = ((square_center_x - circle_x) ** 2 + (square_center_y - circle_y) ** 2) ** 0.5
    if distance <= circle_radius:
        return True
    return False

# Carpeta para guardar los frames temporales
output_folder = 'frames_temp'
os.makedirs(output_folder, exist_ok=True)
frame_count = 0

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Dibujar la figura principal
    if figura == 'cuadrado':
        pygame.draw.rect(screen, PRIMARY_COLOR, (fig_x, fig_y, dimension, dimension), 2)
    elif figura == 'rectangulo':
        pygame.draw.rect(screen, PRIMARY_COLOR, (fig_x, fig_y, width, height), 2)
    elif figura == 'circulo':
        pygame.draw.circle(screen, PRIMARY_COLOR, (circle_x, circle_y), width // 2, 2)

    # Dibujar el círculo secundario
    pygame.draw.circle(screen, SECONDARY_COLOR, (circle_x, circle_y), circle_radius, 2)

    current_time = pygame.time.get_ticks()

    if current_time - last_time >= interval:
        last_time = current_time

        side_length = user_size * 10  # Ajustar tamaño de cuadrado según la entrada del usuario
        initial_direction = random.choice(['up', 'down', 'left', 'right'])
        new_square = [fig_x + width // 2 - side_length // 2, fig_y + height // 2 - side_length // 2, side_length, initial_direction, False]
        cuadrados.append(new_square)
        cuadrados_generados += 1

        for square in cuadrados:
            x, y, size, direction, stopped = square

            if not stopped:
                if random.random() < 0.4:
                    direction = random.choice(['up', 'down', 'left', 'right'])

                if direction == 'up':
                    y -= 10
                elif direction == 'down':
                    y += 10
                elif direction == 'left':
                    x -= 10
                elif direction == 'right':
                    x += 10

                if check_collision_with_figure(x, y, size) or check_collision_with_stopped_squares(x, y, size):
                    stopped = True

                square[0], square[1], square[3], square[4] = x, y, direction, stopped

    for square in cuadrados:
        x, y, size, direction, stopped = square
        pygame.draw.rect(screen, PRIMARY_COLOR, (x, y, size, size))

        if stopped and check_collision_with_red_circle(x, y, size):
            running = False

    # Renderizar texto de tiempo y cuadrados generados
    font = pygame.font.SysFont(None, 36)
    text = font.render("TP9: Tomás Licciardi", True, TEXT_COLOR)
    screen.blit(text, (375, 10))
    text = font.render(f'Cuadrados generados: {cuadrados_generados}', True, TEXT_COLOR)
    screen.blit(text, (10, 40))

    pygame.display.flip()
    pygame.time.delay(33)  # Aproximadamente 30 FPS

    # Guardar el frame actual como imagen
    frame_filename = os.path.join(output_folder, f'frame_{frame_count:05d}.png')
    pygame.image.save(screen, frame_filename)
    frame_count += 1

# Liberar recursos y cerrar Pygame
pygame.quit()

# Crear video a partir de los frames guardados
print("Creando video...")

# Obtener la lista de archivos de los frames
frames = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.png')]
frames.sort()  # Ordenar los frames por orden alfabético

# Configurar el video con OpenCV
video_filename = 'animacion_cuadrado.avi'
frame = cv2.imread(frames[0])
height, width, layers = frame.shape
video = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'DIVX'), 30, (width, height))

# Escribir cada frame en el video
for frame in frames:
    video.write(cv2.imread(frame))

# Liberar recursos de OpenCV
cv2.destroyAllWindows()
video.release()

print(f"Video guardado como '{video_filename}'")

# Eliminar los frames temporales
for frame in frames:
    os.remove(frame)
os.rmdir(output_folder)

sys.exit()
