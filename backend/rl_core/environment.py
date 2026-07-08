import numpy as np

class Environment:
    def __init__(self):
        self.paso_actual = 0
        self.maximo_pasos = 50 # duración de un episodio
        self.anomalia_activa = False
        self.estado_actual = None

    def _get_estado(self):
        # Simula los sensores del entorno y devuelve las variables [velocidad_promedio, densidad_trafico]
        if np.random.rand() < 0.15: # 15% de probabilidad de que ocurra una anomalía
            self.anomalia_activa = True
        else:
            self.anomalia_activa = False
        
        if self.anomalia_activa:
            velocidad_promedio = np.random.uniform(0, 20) # km/h, velocidad muy baja debido a la anomalía
            densidad_trafico = np.random.uniform(80, 100) # % de ocupacion, tráfico muy denso
        else:
            velocidad_promedio = np.random.uniform(40, 80) # km/h, velocidad normal
            densidad_trafico = np.random.uniform(20, 60) # % de ocupacion, tráfico moderado
        
        return {"velocidad_promedio": velocidad_promedio, "densidad_trafico": densidad_trafico, "anomalia_activa": self.anomalia_activa}
    
    def reset(self):
        # Reinicia el entorno para un nuevo episodio
        self.paso_actual = 0
        self.estado_actual = self._get_estado()
        return self.estado_actual
    
    def paso(self, accion):
        # Simula un paso en el entorno basado en la acción tomada por el agente
        anomalia = self.estado_actual["anomalia_activa"]

        # Calcula la recompensa basada en la acción y el estado actual
        reward = 0
        if anomalia and accion == 1:  # Verdadero positivo: el agente detecta correctamente la anomalía
            reward = 10  # Recompensa positiva por tomar la acción correcta
        elif not anomalia and accion == 1:  # Falso positivo: el agente detecta una anomalía inexistente
            reward = -5  # Penalización por tomar la acción incorrecta
        elif anomalia and accion == 0:  # Falso negativo: el agente no detecta la anomalía
            reward = -10  # Penalización por no detectar la anomalía
        else:  # Verdadero negativo: el agente no detecta una anomalía inexistente
            reward = 5  # Recompensa por no tomar acción innecesaria

        self.paso_actual += 1
        done = self.paso_actual >= self.maximo_pasos  # El episodio termina si se alcanza el número máximo de pasos
        self.estado_actual = self._get_estado()  # Actualiza el estado del entorno para el siguiente paso

        return self.estado_actual, reward, done
    
