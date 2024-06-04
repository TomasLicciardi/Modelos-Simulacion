import random
import matplotlib.pyplot as plt
import math
import numpy as np

# Clase Proyecto y sus métodos como en tu código original...
class Proyecto:
    capacidad_calorifica = 4186  # J/kg°C

    def __init__(self, temperatura_inicial, temperatura_final, temperatura_exterior, resistencia=None,voltaje=None):
        self.temperatura_inicial = temperatura_inicial  # °C
        self.temperatura_final = temperatura_final  # °C
        self.temperatura_exterior = temperatura_exterior  # °C
        self.capacidad = 1000  # Gramos (volumen de agua en el cilindro)
        self.voltaje = voltaje if voltaje is not None else 220  # Voltios
        self.tiempo = 240  # Segundos
        self.altura = 35  # cm
        self.radio = 8  # cm
        self.espesor = 0.001  # Metros
        self.conductividad_de_telgopor = 0.035  # Conductividad térmica del telgopor
        self.superficie = (
            (2 * math.pi * (self.radio ** 2) + 2 * math.pi * self.radio * self.altura) / 10000
        )  # Área de la superficie del cilindro
        self.resistencia = resistencia
        self.voltaje = voltaje
        self.descenso_activo = False
        self.segundos_restantes = 0
        self.temperatura_exterior_normal = temperatura_exterior

    # Métodos para cálculos
    def calcular_calor(self):
        masa = self.capacidad/1000
        variacion_temperatura = self.temperatura_final - self.temperatura_inicial
        calor = masa * self.capacidad_calorifica * variacion_temperatura
        return calor
    
    def calcular_potencia(self):
        if self.resistencia:
            potencia = ((self.voltaje ** 2) / self.resistencia)
        else:
            potencia = self.calcular_calor() / self.tiempo
        return potencia 
    
    def temperatura_por_segundo(self):
        potencia = self.calcular_potencia()
        aumento_temperatura = potencia / ((self.capacidad/1000) * self.capacidad_calorifica)
        return aumento_temperatura
    
    def obtener_temperaturas_sin_perdida(self):
        segundos = []
        temperaturas = []
        for seg in range(self.tiempo + 1):
            temperatura = self.temperatura_inicial + self.temperatura_por_segundo() * seg
            segundos.append(seg)
            temperaturas.append(temperatura)
        
        return segundos, temperaturas

    def obtener_temperaturas_con_perdida(self):
        segundos = []
        temperaturas = []
        temperatura_actual = self.temperatura_inicial
        tiempo = 0
        while temperatura_actual <= 80:
            if self.descenso_activo:
                if self.segundos_restantes > 0:
                    self.segundos_restantes -= 1
                else:
                    self.temperatura_exterior = self.temperatura_exterior_normal
                    self.descenso_activo = False
                tiempo += 1
            else:
                num_aleatorio = random.randint(1,300)
                if num_aleatorio == 1:
                    descenso_temperatura = random.randint(-50, 0)
                    duracion= random.randint(1, 40)
                    self.temperatura_exterior = descenso_temperatura
                    self.segundos_restantes = duracion
                    self.descenso_activo = True
                tiempo += 1
            
            calor_perdido = (self.conductividad_de_telgopor * self.superficie * (temperatura_actual - self.temperatura_exterior) / self.espesor)
            variacion_temperatura = self.temperatura_por_segundo() - (calor_perdido / self.capacidad_calorifica)
            temperatura_actual += variacion_temperatura
            segundos.append(tiempo)
            temperaturas.append(temperatura_actual)
        
        return segundos, temperaturas

def main():
    temperatura_inicial = 20
    temperatura_final = 80
    temperatura_exterior = 20
    '''
    resistencias = np.random.uniform(40, 50, 5)
    temperaturas_iniciales = np.random.normal(10, 5, 5)
    temperaturas_exteriores = np.random.uniform(-20,50,5)
    voltajes = np.random.normal(220, 40, 5)
    '''
    opcion = int(input("1 para temperatura sin pérdida o 2 para temperatura con pérdida de calor: "))
    
    proyecto = Proyecto(temperatura_inicial,temperatura_final ,temperatura_exterior)
    if opcion == 1:
        segundos, temperaturas = proyecto.obtener_temperaturas_sin_perdida()
        plt.plot(segundos, temperaturas)
    elif opcion == 2:
        segundos, temperaturas = proyecto.obtener_temperaturas_con_perdida()
        plt.plot(segundos, temperaturas)

    # Configuración del gráfico
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Gráfico de Temperatura")
    plt.legend() 
    plt.show() 

if __name__ == "__main__":
    main()
