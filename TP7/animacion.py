import pygame
import random
import numpy as np
import threading
import cv2
import os

class Cliente:
 
    def __init__(self, tiempo_llegada):
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_atencion = None
        self.tiempo_salida = None
        self.tiempo_espera = None

class Box:
    def __init__(self):
        self.ocupado = False
        self.cliente_actual = None
        self.tiempo_inicio_atencion = None

class Local:
    def __init__(self, cantidad_boxes, fps):
        self.cantidad_boxes = cantidad_boxes
        self.boxes = [Box() for _ in range(cantidad_boxes)]
        self.fps = fps
        self.cola = []
        self.clientes_atendidos = 0
        self.clientes_abandonados = 0
        self.tiempo_inicio_operacion = None
        self.tiempo_fin_operacion = None
        self.tiempo_min_atencion = float('inf')
        self.tiempo_max_atencion = 0
        self.tiempo_min_espera = float('inf')
        self.tiempo_max_espera = 0

    def simular(self):
        self.tiempo_inicio_operacion = 0 
        self.tiempo_fin_operacion = 14400  

        tiempo_actual = self.tiempo_inicio_operacion

        while tiempo_actual < self.tiempo_fin_operacion:
            if random.random() < 1/144:
                cliente = Cliente(tiempo_actual)
                self.cola.append(cliente)

            for i, box in enumerate(self.boxes):
                if not box.ocupado and self.cola:
                    cliente = self.cola.pop(0)
                    box.ocupado = True
                    box.cliente_actual = cliente
                    box.tiempo_inicio_atencion = tiempo_actual
                    cliente.tiempo_atencion = max(0, np.random.normal(loc=600, scale=300)) 

            for i, box in enumerate(self.boxes):
                if box.ocupado:
                    tiempo_restante_atencion = box.cliente_actual.tiempo_atencion - (tiempo_actual - box.tiempo_inicio_atencion)
                    if tiempo_restante_atencion <= 0:
                        box.ocupado = False
                        box.cliente_actual.tiempo_salida = tiempo_actual
                        box.cliente_actual.tiempo_espera = box.cliente_actual.tiempo_salida - box.cliente_actual.tiempo_llegada
                        self.clientes_atendidos += 1

                       
                        self.tiempo_min_atencion = min(self.tiempo_min_atencion, box.cliente_actual.tiempo_atencion)
                        self.tiempo_max_atencion = max(self.tiempo_max_atencion, box.cliente_actual.tiempo_atencion)

                       
                        self.tiempo_min_espera = min(self.tiempo_min_espera, box.cliente_actual.tiempo_espera)
                        self.tiempo_max_espera = max(self.tiempo_max_espera, box.cliente_actual.tiempo_espera)

                    elif box.cliente_actual.tiempo_llegada + 1800 < tiempo_actual:
                        box.ocupado = False
                        self.clientes_abandonados += 1  
            
            for i in range(len(self.cola) - 1, -1, -1):
                if self.cola[i].tiempo_llegada + 1800 < tiempo_actual:
                    self.cola.pop(i)
                    self.clientes_abandonados += 1

            if tiempo_actual % 100 == 0:  
                self.actualizar_pantalla(tiempo_actual)

            tiempo_actual += 1 

        self.clientes_abandonados += len(self.cola)

    def calcular_costo(self):
        costo_boxes = self.cantidad_boxes * 1000  
        costo_perdida_clientes = self.clientes_abandonados * 10000  
        costo_total = costo_boxes + costo_perdida_clientes
        return costo_total

    def actualizar_pantalla(self, tiempo_actual):
        with screen_lock:
            screen.fill((20, 20, 20)) 

            x_boxes = 900
            y_boxes = 50
            for i, box in enumerate(self.boxes):
                color = (255, 0, 0) if box.ocupado else (0, 255, 0)  
                pygame.draw.rect(screen, color, (x_boxes, y_boxes + i * 100, 80, 80), 15)  # Aumentar grosor del borde a 5
                font = pygame.font.SysFont(None, 30)
                text = font.render(f"Box {i + 1}", True, (255, 255, 255))  
                text_rect = text.get_rect(center=(x_boxes + 40, y_boxes + i * 100 + 40))
                screen.blit(text, text_rect)


            x_cola = 650   
            y_cola = 150  

            radio_circulo = 15
            for i, cliente in enumerate(self.cola):
                pygame.draw.circle(screen, (255, 255, 0), (x_cola, y_cola + i * (radio_circulo * 2 + 10)), radio_circulo)  

            font = pygame.font.SysFont(None, 23)
            textos = [
                f"Clientes Ingresados: {self.clientes_atendidos + self.clientes_abandonados}",
                f"Clientes Atendidos: {self.clientes_atendidos}",
                f"Clientes Perdidos: {self.clientes_abandonados}",
                f"Tiempo Máximo Atención: {self.tiempo_max_atencion // 60}m",
                f"Tiempo Mínimo Atención: {self.tiempo_min_atencion // 60}m",
                f"Tiempo Máximo Espera: {self.tiempo_max_espera // 60}m",
                f"Tiempo Mínimo Espera: {self.tiempo_min_espera // 60}m",
                f"Costo Boxes: {self.cantidad_boxes * 1000}",
                f"Costo Clientes Perdidos: {self.clientes_abandonados * 10000}",
                f"Costo Total: {self.calcular_costo()}"
            ]

            for i, texto in enumerate(textos):
                img = font.render(texto, True, (255, 255, 255)) 
                screen.blit(img, (50, 150 + i * 30))  

            pygame.display.flip()
            clock.tick(self.fps)  

if __name__ == "__main__":
    
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Simulación de Boxes de Atención")
    clock = pygame.time.Clock()
    
    local = Local(5, 100)

    nombre_archivo = "animacion_5_boxes.avi"
    contador = 2
    while os.path.exists(nombre_archivo):
        nombre_archivo = f"animacion_5_boxes{contador}.avi"
        contador += 1

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(nombre_archivo, fourcc, local.fps, (1200, 600))

    grabando = True

    screen_lock = threading.Lock()

    simulation_thread = threading.Thread(target=local.simular)
    simulation_thread.start()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        with screen_lock:
            
            if grabando and simulation_thread.is_alive():
                
                frame = np.array(pygame.surfarray.pixels3d(screen))
                frame = frame.swapaxes(0, 1)  
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 

                out.write(frame)
            else:
                grabando = False 

                
                pygame.time.delay(500)  
                running = False  
    
    simulation_thread.join()  

    out.release() 
    pygame.quit()