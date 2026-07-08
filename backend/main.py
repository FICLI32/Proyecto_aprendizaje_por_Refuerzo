from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rl_core.environment import Environment
from rl_core.agent import Agent

app = FastAPI(title="Sistema de Control de Tráfico Inteligente RL")

# Configuración de CORS para que el frontend pueda comunicarse con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Instancia del entorno y del agente
entorno = Environment()
agente = Agent()

# Estado inicial del entorno
estado_actual = entorno.reset()

class ParametrosEntrenamiento(BaseModel):
    episodios: int = 1000

@app.get("/")
def leer_origen():
    return {"mensaje": "Bienvenido al Sistema de Control de Tráfico Inteligente RL"}

@app.post("/entrenar")
def entrenar_agente(parametros: ParametrosEntrenamiento):
    # Entrenar al agente con el número de episodios especificado
    global agente 

    agente = Agent()  # Reiniciar el agente para un nuevo entrenamiento

    recompensa_por_episodio = [] 

    for episodio in range(parametros.episodios):
        estado_actual = entorno.reset()
        done = False
        recompensa_episodio = 0

        while not done:
            accion = agente.seleccionar_accion(estado_actual)
            estado_nuevo, recompensa, done = entorno.paso(accion)
            agente.aprender(estado_actual, accion, recompensa, estado_nuevo)
            estado_actual = estado_nuevo
            recompensa_episodio += recompensa

        agente.decaimiento_exploracion(episodio)
        recompensa_por_episodio.append(recompensa_episodio)
    
    return {
        "mensaje": f"Entrenamiento completado en {parametros.episodios} episodios completado.",
        "recompensa_media_final": sum(recompensa_por_episodio[-100:]) / 100,
        "q_table_final": agente.q_table.tolist()  # Convertir la tabla Q a lista para JSON
    }

@app.get("/simular_paso")
def simular_paso():
    # Ejecutae un paso de simulación usando lo que el agente ha aprendido
    global estado_actual
    
    # 1. Explotación total
    epsilon_temporal = agente.epsilon
    agente.epsilon = 0.0 
    
    # 2. El agente toma la decisión
    accion = agente.seleccionar_accion(estado_actual)
    
    # 3. Restaurar el epsilon
    agente.epsilon = epsilon_temporal
    
    # 4. Reaccion del entorno y obtención de la recompensa
    estado_nuevo, recompensa, done = entorno.paso(accion)
    
    # almacenar el estado del paso anterior 
    estado_previo = estado_actual
    estado_actual = estado_nuevo
    
    if done:
        estado_actual = entorno.reset()
        
    return {
        "estado_observado": estado_previo,
        "accion_tomada": "Mantener" if accion == 0 else "Desviar",
        "recompensa_obtenida": recompensa,
        "nuevo_estado": estado_actual,
        "episodio_terminado": done
    }