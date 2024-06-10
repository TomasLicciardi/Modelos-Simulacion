import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animación de Cuadrados")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configuración del círculo y los cuadrados
CIRCLE_RADIUS = 50
SQUARE_SIZE = 40  # Ajuste del tamaño del cuadrado para una mejor visibilidad
CENTER = (WIDTH // 2, HEIGHT // 2)

# Tiempo aleatorio entre 0.2 y 1 segundo
MIN_TIME = 200
MAX_TIME = 1000

# Función para dibujar el círculo
def draw_circle():
    pygame.draw.circle(screen, BLACK, CENTER, CIRCLE_RADIUS, 2)

# Clase para los cuadrados
class Square:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = SQUARE_SIZE
        self.color = RED
        self.stuck = False
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
    def move(self):
        if not self.stuck:
            direction = random.choice(['up', 'down', 'left', 'right'])
            if direction == 'up' and self.y > 0:
                self.y -= self.size
            elif direction == 'down' and self.y < HEIGHT - self.size:
                self.y += self.size
            elif direction == 'left' and self.x > 0:
                self.x -= self.size
            elif direction == 'right' and self.x < WIDTH - self.size:
                self.x += self.size

# Lista de cuadrados
squares = []

# Función para verificar la condición de finalización
def check_end_condition():
    for square in squares:
        if square.stuck:
            distance_to_center = math.sqrt((square.x + square.size // 2 - WIDTH // 2) ** 2 + (square.y + square.size // 2 - HEIGHT // 2) ** 2)
            if distance_to_center <= CIRCLE_RADIUS:
                return True
    return False

# Función principal
def main():
    running = True
    clock = pygame.time.Clock()
    time_to_next_square = random.randint(MIN_TIME, MAX_TIME)

    while running:
        screen.fill(WHITE)
        draw_circle()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Generar nuevos cuadrados con tiempo aleatorio
        time_to_next_square -= clock.get_time()
        if time_to_next_square <= 0:
            squares.append(Square())
            time_to_next_square = random.randint(MIN_TIME, MAX_TIME)
        
        # Mover y dibujar cuadrados
        for square in squares:
            square.move()
            square.draw()

            # Chequear colisiones con paredes
            if square.x <= 0 or square.x >= WIDTH - square.size or square.y <= 0 or square.y >= HEIGHT - square.size:
                square.stuck = True
            
            # Chequear colisiones con otros cuadrados pegados
            for other_square in squares:
                if other_square != square and other_square.stuck:
                    if abs(square.x - other_square.x) < square.size and abs(square.y - other_square.y) < square.size:
                        square.stuck = True

        # Verificar si la simulación debe terminar
        if check_end_condition():
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
