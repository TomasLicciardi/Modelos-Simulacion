import matplotlib.pyplot as plt
import math

class Proyecto:
    capacidad_calorifica = 4186 # J/kg°C

    def __init__(self, temperatura_inicial, temperatura_final,temperatura_exterior):
        self.capacidad = 1000                            # Gramos(volumen de agua en el cilindro)
        self.temperatura_inicial = temperatura_inicial   # °C
        self.temperatura_final = temperatura_final       # °C
        self.temperatura_exterior = temperatura_exterior # °C
        self.voltaje = 220                               # Voltaje
        self.tiempo = 240                                # Segundos
        self.altura = 35                                 # cm
        self.radio = 8                                   # cm
        self.espesor = 0.001                             # Metros
        self.conductividad_de_telgopor = 0.035                                 # Conductividad térmica del telgopor
        self.superficie = (2 * math.pi * (self.radio**2) + 2 * math.pi * self.radio * self.altura)/10000 #Area de la superficie del cilindro

    def calcular_calor(self):
        masa = self.capacidad
        variacion_temperatura = self.temperatura_final - self.temperatura_inicial
        calor = masa * self.capacidad_calorifica * variacion_temperatura
        return calor
    
    def calcular_potencia(self):
        potencia = self.calcular_calor() / self.tiempo
        return potencia
    
    def calcular_intensidad(self):
        intensidad = self.calcular_potencia() / self.voltaje
        return intensidad
    
    def calcular_resistencia(self):
        resistencia = self.voltaje / self.calcular_intensidad()
        return resistencia
    
    def temperatura_por_segundo(self):
        potencia = self.calcular_potencia()
        aumento_temperatura = potencia / (self.capacidad * self.capacidad_calorifica)
        return aumento_temperatura

    def obtener_temperaturas_sin_perdida(self):
        segundos = []
        temperaturas_sin_perdida = []
        for seg in range(self.tiempo + 1):
            temperatura = self.temperatura_inicial + self.temperatura_por_segundo() * seg
            segundos.append(seg)
            temperaturas_sin_perdida.append(temperatura)
        
        return segundos, temperaturas_sin_perdida


    def obtener_temperaturas_con_perdida(self):
        segundos = []
        temperaturas_con_perdida = []
        temperatura_actual = self.temperatura_inicial

        for seg in range(self.tiempo + 1):
            print(seg)
            calor_perdido = self.conductividad_de_telgopor * self.superficie * (temperatura_actual - self.temperatura_exterior) / self.espesor
            print(calor_perdido)
            variacion_temperatura = self.temperatura_por_segundo() - (calor_perdido / self.capacidad_calorifica)
            segundos.append(seg)
            temperatura_actual += variacion_temperatura
            temperaturas_con_perdida.append(temperatura_actual)
        print(temperaturas_con_perdida)
        return segundos, temperaturas_con_perdida


    def graficar_temperatura_sin_perdida(self):
        segundos, temperaturas_sin_perdida = self.obtener_temperaturas_sin_perdida()
        plt.plot(segundos, temperaturas_sin_perdida)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura del Líquido sin pérdida de calor')
        plt.show()

    def graficar_temperatura_con_perdida(self):
        segundos, temperaturas_con_perdida = self.obtener_temperaturas_con_perdida()
        plt.plot(segundos, temperaturas_con_perdida)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Temperatura del Líquido con pérdida de calor')
        plt.show()

def main():
    cantidad_proyectos = int(input("Ingrese la cantidad de proyectos a realizar: "))
    proyectos = []
    for i in range(cantidad_proyectos):
        print(f"Proyecto {i + 1}")
        while True:
            try:
                temperatura_inicial = int(input("Ingrese la temperatura inicial (en °C): "))
                if temperatura_inicial < 0:
                    raise ValueError("La temperatura inicial no puede ser negativa.")
                break
            except ValueError as e:
                print(e)
        
        while True:
            try:
                temperatura_final = int(input("Ingrese la temperatura final (en °C): "))
                if temperatura_final < 0:
                    raise ValueError("La temperatura final no puede ser negativa.")
                break
            except ValueError as e:
                print(e)
        
        while True:
            try:
                temperatura_exterior = int(input("Ingrese la temperatura exterior (en °C): "))
                if temperatura_exterior < 0:
                    raise ValueError("La temperatura exterior no puede ser negativa.")
                break
            except ValueError as e:
                print(e)
        
        proyecto = Proyecto(temperatura_inicial, temperatura_final, temperatura_exterior)
        proyectos.append(proyecto)
    plt.figure()
    for pr in proyectos:
        pr.graficar_temperatura_sin_perdida()
        pr.graficar_temperatura_con_perdida()

if __name__ == '__main__':
    main()
