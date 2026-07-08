import numpy as np
import random

class Agent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, max_exploration_rate=1.0, min_exploration_rate=0.01, exploration_decay_rate=0.01):
        # Parametros de aprendizaje
        self.learning_rate = learning_rate
        self.gamma = discount_factor

        # Parametros de exploracion (Epsilon-greedy)
        self.epsilon = exploration_rate
        self.max_epsilon = max_exploration_rate
        self.min_epsilon = min_exploration_rate
        self.epsilon_decay = exploration_decay_rate

        self.q_table = np.zeros((9, 2)) # 9 estados posibles (combinaciones de velocidad y densidad) y 2 acciones posibles (mantener o desviar)

    def discretizar_estado(self, estado):
        # Logica para combertir el estado continuo en un estado discreto (0-8)
        velocidad = estado["velocidad_promedio"]
        densidad = estado["densidad_trafico"]

        # Velocidad discretizada (0: lenta, 1: media, 2: alta)
        if velocidad < 30: v_index = 0
        elif velocidad < 60: v_index = 1
        else: v_index = 2

        # Densidad discretizada (0: baja, 1: media, 2: alta)
        if densidad < 40: d_index = 0
        elif densidad < 80: d_index = 1
        else: d_index = 2

        # Combinar los índices para obtener el estado discreto (0-8)
        state_idx = (v_index * 3) + d_index
        return state_idx
    
    def seleccionar_accion(self, estado_discreto):
        # Accion basada en la polita Epsilon-greedy
        estado_discreto = self.discretizar_estado(estado_discreto)

        if random.uniform(0, 1) < self.epsilon:
            # Exploracion: seleccionar una accion aleatoria
            return random.choice([0, 1])  # 0: mantener, 1: desviar
        else:
            # Explotacion: seleccionar la accion con el mayor valor Q
            return np.argmax(self.q_table[estado_discreto, :])
        
    def aprender(self, estado_discreto_antiguo, accion, recompensa, estado_discreto_nuevo):
        # Actualizar la tabla Q usando la ecuacion de Q-learning
        estado_discreto_antiguo = self.discretizar_estado(estado_discreto_antiguo)
        estado_discreto_nuevo = self.discretizar_estado(estado_discreto_nuevo)

        # Valor Q actual
        q_actual = self.q_table[estado_discreto_antiguo, accion]

        # Valor Q maximo para el nuevo estado
        q_max_nuevo = np.max(self.q_table[estado_discreto_nuevo, :])

        # Actualizacion de la tabla Q
        nuevo_valor = q_actual + self.learning_rate * (recompensa + self.gamma * q_max_nuevo - q_actual)
        self.q_table[estado_discreto_antiguo, accion] = nuevo_valor

    def decaimiento_exploracion(self, episodio):
        # Reducir la tasa de exploracion (epsilon) para que el agente empiece a explotar lo aprendido
        self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.epsilon_decay * episodio)
