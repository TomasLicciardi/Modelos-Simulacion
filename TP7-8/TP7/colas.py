'''TP7 - Simulación de colas de atención al público'''
import numpy as np
import random
import queue
import matplotlib.pyplot as plt

# Constantes y parámetros
HORAS_OPERACION = 4  # 8 a 12 horas = 4 horas
SEGUNDOS_POR_HORA = 3600
TIEMPO_TOTAL_SEGUNDOS = HORAS_OPERACION * SEGUNDOS_POR_HORA
PROBABILIDAD_INGRESO = 1 / 144
MEDIA_ATENCION = 10 * 60  # en segundos
DESVIO_STD_ATENCION = 5 * 60  # en segundos
COSTO_BOX = 1000
COSTO_ABANDONO = 10000
TIEMPO_MAX_ESPERA = 30 * 60  # en segundos

class Cliente:
    def __init__(self, tiempo_llegada):
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_atencion_inicio = None
        self.tiempo_atencion_fin = None
        self.abandonado = False

    def tiempo_espera(self):
        if self.tiempo_atencion_inicio is None:
            return None
        return self.tiempo_atencion_inicio - self.tiempo_llegada

    def tiempo_atencion(self):
        if self.tiempo_atencion_inicio is None or self.tiempo_atencion_fin is None:
            return None
        return self.tiempo_atencion_fin - self.tiempo_atencion_inicio

class Simulacion:
    def __init__(self, num_boxes):
        self.num_boxes = num_boxes
        self.boxes = [None] * num_boxes
        self.cola = queue.Queue()
        self.clientes = []
        self.clientes_por_intervalo = [0] * (HORAS_OPERACION * 2)  # Lista para registrar los clientes por intervalos de 30 minutos

    def run(self):
        segundo = 0
        for segundo in range(TIEMPO_TOTAL_SEGUNDOS):
            self.ingresar_cliente(segundo)
            self.actualizar_boxes(segundo)
            self.actualizar_cola(segundo)
        
        while any(box is not None for box in self.boxes) or not self.cola.empty():
            segundo += 1
            self.actualizar_boxes(segundo)
            self.actualizar_cola(segundo)

    def ingresar_cliente(self, segundo):
        if random.random() < PROBABILIDAD_INGRESO:
            cliente = Cliente(segundo)
            self.clientes.append(cliente)
            self.cola.put(cliente)
            intervalo = segundo // (SEGUNDOS_POR_HORA // 2)
            if intervalo < len(self.clientes_por_intervalo):
                self.clientes_por_intervalo[intervalo] += 1

    def actualizar_boxes(self, segundo):
        for i in range(self.num_boxes):
            if self.boxes[i] is not None:
                cliente = self.boxes[i]
                if cliente.tiempo_atencion_fin <= segundo:
                    self.boxes[i] = None  # Box libre
            if self.boxes[i] is None and not self.cola.empty():
                cliente = self.cola.get()
                cliente.tiempo_atencion_inicio = segundo
                tiempo_atencion = max(1, int(np.random.normal(MEDIA_ATENCION, DESVIO_STD_ATENCION)))
                cliente.tiempo_atencion_fin = segundo + tiempo_atencion
                self.boxes[i] = cliente

    def actualizar_cola(self, segundo):
        size = self.cola.qsize()
        for _ in range(size):
            cliente = self.cola.get()
            if segundo - cliente.tiempo_llegada >= TIEMPO_MAX_ESPERA:
                cliente.abandonado = True
            else:
                self.cola.put(cliente)
                break

def calcular_resultados(simulacion):
    clientes_ingresados = len(simulacion.clientes)
    clientes_atendidos = sum(1 for cliente in simulacion.clientes if cliente.tiempo_atencion_fin is not None)
    clientes_no_atendidos = sum(1 for cliente in simulacion.clientes if cliente.abandonado)
    tiempos_atencion = [cliente.tiempo_atencion() for cliente in simulacion.clientes if cliente.tiempo_atencion() is not None]
    tiempos_espera = [cliente.tiempo_espera() for cliente in simulacion.clientes if cliente.tiempo_espera() is not None]
    
    if tiempos_atencion:
        tiempo_min_atencion = min(tiempos_atencion)
        tiempo_max_atencion = max(tiempos_atencion)
    else:
        tiempo_min_atencion = tiempo_max_atencion = None
    
    if tiempos_espera:
        tiempo_min_espera = min(tiempos_espera)
        tiempo_max_espera = max(tiempos_espera)
    else:
        tiempo_min_espera = tiempo_max_espera = None
    
    costo_boxes = simulacion.num_boxes * COSTO_BOX
    costo_abandono = clientes_no_atendidos * COSTO_ABANDONO
    costo_operacion = costo_boxes + costo_abandono

    resultados = {
        "clientes_ingresados": clientes_ingresados,
        "clientes_atendidos": clientes_atendidos,
        "clientes_no_atendidos": clientes_no_atendidos,
        "tiempo_min_atencion": tiempo_min_atencion,
        "tiempo_max_atencion": tiempo_max_atencion,
        "tiempo_min_espera": tiempo_min_espera,
        "tiempo_max_espera": tiempo_max_espera,
        "costo_operacion": costo_operacion,
        "costo_boxes": costo_boxes,
        "costo_abandono": costo_abandono,
        "clientes": simulacion.clientes,
        "clientes_por_intervalo": simulacion.clientes_por_intervalo  # Añadir clientes por intervalo a los resultados
    }
    
    return resultados

def graficar_resultados(resultados):
    # Crear una nueva figura para la gráfica de clientes por intervalos de 30 minutos
    plt.figure()
    intervalos = ['8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30']
    clientes_por_intervalo = resultados['clientes_por_intervalo']
    plt.bar(intervalos, clientes_por_intervalo, color='blue', edgecolor='black')
    plt.xlabel('Intervalo de Tiempo')
    plt.ylabel('Cantidad de Clientes')
    plt.title('Cantidad de Clientes Ingresados por Intervalo de 30 Minutos')
    plt.grid(True)
    plt.show()
    
    # Crear la figura principal
    plt.figure(figsize=(14, 10))
    
    categorias = ['Ingresados', 'Atendidos', 'No Atendidos']
    valores = [resultados['clientes_ingresados'], resultados['clientes_atendidos'], resultados['clientes_no_atendidos']]
    
    plt.subplot(2, 2, 1)
    plt.bar(categorias, valores, color=['blue', 'green', 'red'])
    plt.xlabel('Categoría')
    plt.ylabel('Cantidad de Clientes')
    plt.title('Clientes Ingresados, Atendidos y No Atendidos')
    
    tiempos_atencion = [cliente.tiempo_atencion() for cliente in resultados['clientes'] if cliente.tiempo_atencion() is not None]
    plt.subplot(2, 2, 2)
    plt.hist(tiempos_atencion, bins=20, color='purple', edgecolor='black')
    plt.xlabel('Tiempo de Atención (segundos)')
    plt.ylabel('Clientes')
    plt.title('Distribución de Tiempos de Atención')
    
    tiempos_espera = [cliente.tiempo_espera() for cliente in resultados['clientes'] if cliente.tiempo_espera() is not None]
    plt.subplot(2, 2, 3)
    plt.hist(tiempos_espera, bins=20, color='orange', edgecolor='black')
    plt.xlabel('Tiempo de Espera (segundos)')
    plt.ylabel('Clientes')
    plt.title('Distribución de Tiempos de Espera')
    
    categorias_costos = ['Costo de Boxes', 'Costo de Abandono']
    valores_costos = [resultados['costo_boxes'], resultados['costo_abandono']]
    
    plt.subplot(2, 2, 4)
    plt.bar(categorias_costos, valores_costos, color=['cyan', 'magenta'])
    plt.xlabel('Categoría')
    plt.ylabel('Costo ($)')
    plt.title('Costos de Operación')
    
    plt.tight_layout()
    plt.show()

def main():
    num_boxes = 5
    simulacion = Simulacion(num_boxes)
    simulacion.run()
    resultados = calcular_resultados(simulacion)
    
    print("Resultados de la simulación:")
    print(f"Clientes ingresados: {resultados['clientes_ingresados']}")
    print(f"Clientes atendidos: {resultados['clientes_atendidos']}")
    print(f"Clientes no atendidos: {resultados['clientes_no_atendidos']}")
    print(f"Tiempo mínimo de atención: {resultados['tiempo_min_atencion']} segundos")
    print(f"Tiempo máximo de atención: {resultados['tiempo_max_atencion']} segundos")
    print(f"Tiempo mínimo de espera: {resultados['tiempo_min_espera']} segundos")
    print(f"Tiempo máximo de espera: {resultados['tiempo_max_espera']} segundos")
    print(f"Costo de la operación: ${resultados['costo_operacion']}")
    
    graficar_resultados(resultados)
    
if __name__ == "__main__":
    main()
