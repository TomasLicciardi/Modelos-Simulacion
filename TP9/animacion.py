import pygame
import sys
import random
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

# Dimensiones y coordenadas de la figura principal (cuadrado)
fig_width = fig_height = 300
fig_x = (width - fig_width) // 2
fig_y = (height - fig_height) // 2

# Dimensiones del círculo secundario (1/4 del tamaño de la figura principal)
circle_diameter = min(fig_width, fig_height) // 4
circle_radius = circle_diameter // 2

# Coordenadas del círculo secundario (centrado en la ventana)
circle_x = width // 2
circle_y = height // 2

# Lista para almacenar los cuadrados generados
# Cada cuadrado será representado como [x, y, side_length, direction, stopped]
cuadrados = []

# Tiempo de control para generar cuadrados cada segundo (ajustar para simulación rápida)
last_time = pygame.time.get_ticks()
interval = 200  # 200 ms para acelerar la simulación

# Variables para rastrear el tiempo y la cantidad de cuadrados generados
start_ticks = pygame.time.get_ticks()
cuadrados_generados = 0

# Fuente para mostrar texto en la pantalla
font = pygame.font.SysFont(None, 36)

# Configuración de OpenCV para guardar el video
output_filename = "animacion_figuras3.avi"
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

# Función para verificar si un cuadrado toca el borde del cuadrado principal
def check_collision_with_figure(x, y, size):
    if (x <= fig_x or x + size >= fig_x + fig_width or 
        y <= fig_y or y + size >= fig_y + fig_height):
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

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Dibujar el cuadrado principal
    pygame.draw.rect(screen, PRIMARY_COLOR, (fig_x, fig_y, fig_width, fig_height), 2)

    # Dibujar el círculo secundario
    pygame.draw.circle(screen, SECONDARY_COLOR, (circle_x, circle_y), circle_radius, 2)

    current_time = pygame.time.get_ticks()

    if current_time - last_time >= interval:
        last_time = current_time

        side_length = 20
        initial_direction = random.choice(['up', 'down', 'left', 'right'])
        new_square = [width // 2 - side_length // 2, height // 2 - side_length // 2, side_length, initial_direction, False]
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

    # Calcular segundos transcurridos
    seconds = (current_time - start_ticks) // 1000

    # Renderizar texto de tiempo y cuadrados generados
    text = font.render("TP9: Tomás Licciardi",True, TEXT_COLOR)
    screen.blit(text,(375,10))
    text = font.render(f'Cuadrados generados: {cuadrados_generados}', True, TEXT_COLOR)
    screen.blit(text, (10, 40))

    # Capturar el frame actual con OpenCV
    frame = pygame.surfarray.array3d(screen)
    frame = cv2.cvtColor(frame.swapaxes(0, 1), cv2.COLOR_RGB2BGR)
    video.write(frame)

    pygame.display.flip()
    pygame.time.delay(33)  # Aproximadamente 30 FPS

# Liberar el video y cerrar Pygame
video.release()
pygame.quit()
sys.exit()
