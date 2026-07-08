import numpy as np
from environment import Environment
from agent import Agent

def entrenar_agente(episodios=1000):
    entorno = Environment()
    agente = Agent()

    recompensa_acumulada = 0
    
    print("iniciando entrenamiento del sistema\n")

    for episodio in range(episodios):
        estado_actual = entorno.reset()
        done = False
        recompensa_episodio = 0

        while not done:
            # 1. El agente elige una acción (0: Mantener, 1: Desviar)
            accion = agente.seleccionar_accion(estado_actual)
            
            # 2. El entorno reacciona y devuelve el nuevo estado y la recompensa
            estado_nuevo, recompensa, done = entorno.paso(accion)
            
            # 3. El agente actualiza su Q-Table (aprende)
            agente.aprender(estado_actual, accion, recompensa, estado_nuevo)
            
            # Actualización de estado y acumulación de recompensa
            estado_actual = estado_nuevo
            recompensa_episodio += recompensa

        # 4. Reduccion de la exploración al final de cada episodio
        agente.decaimiento_exploracion(episodio)
        
        recompensa_acumulada += recompensa_episodio

        # Impresion de estadísticas cada 100 episodios
        if (episodio + 1) % 100 == 0:
            recompensa_media = recompensa_acumulada / 100
            print(f"Episodio {episodio + 1}/{episodios} | Recompensa media: {recompensa_media:7.2f} | Tasa de exploración (Epsilon): {agente.epsilon:.3f}")
            recompensa_acumulada = 0

    print("\nQ-Table Final:")
    print("Filas: Estados discretos (0 al 8)")
    print("Columnas: Valores de las acciones [Mantener, Desviar]\n")
    
    # tabla Q con formato
    print(np.round(agente.q_table, 2))

if __name__ == "__main__":
    entrenar_agente()