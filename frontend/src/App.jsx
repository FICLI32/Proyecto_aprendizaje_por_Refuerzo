import { useState } from 'react'
import './App.css'

function App() {
  //  ESTADOS DE NAVEGACIÓN 
  const [vistaActiva, setVistaActiva] = useState('introduccion')

  //  ESTADOS DEL AGENTE RL 
  const [entrenando, setEntrenando] = useState(false)
  const [qTable, setQTable] = useState(null)
  const [simulacion, setSimulacion] = useState(null)
  const [mensaje, setMensaje] = useState("Bienvenido. Entrena al agente para comenzar.")
  
  // Estado para forzar el reinicio de la animación 2D en cada clic
  const [stepId, setStepId] = useState(0)

  // Función para llamar a FastAPI y entrenar al agente
  const entrenarAgente = async () => {
    setEntrenando(true)
    setMensaje("Entrenando al agente... por favor espera.")
    try {
      const response = await fetch("http://127.0.0.1:8000/entrenar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ episodios: 1000 })
      })
      const data = await response.json()
      setQTable(data.q_table_final)
      setMensaje(`¡Entrenamiento exitoso! Recompensa media final: ${data.recompensa_media_final}`)
    } catch (error) {
      setMensaje("Error al conectar con el servidor Backend.")
    }
    setEntrenando(false)
  }

  // Función para simular un paso
  const simularPaso = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/simular_paso")
      const data = await response.json()
      setSimulacion(data)
      setStepId(prev => prev + 1) 
    } catch (error) {
      setMensaje("Error al simular el paso.")
    }
  }

  // Lógica para determinar la animación del auto
  let claseAnimacionAuto = ""
  if (simulacion) {
    const anomalia = simulacion.estado_observado.anomalia_activa
    const accion = simulacion.accion_tomada
    
    if (accion === "Mantener" && !anomalia) claseAnimacionAuto = "auto-recto"
    if (accion === "Mantener" && anomalia) claseAnimacionAuto = "auto-choque"
    if (accion === "Desviar") claseAnimacionAuto = "auto-desvio"
  }

  return (
    <div className="container">
      <header>
        <h1>🚦 Tráfico Inteligente con Reinforcement Learning</h1>
      </header>

      <div className="app-layout">
        {/* BARRA LATERAL */}
        <aside className="sidebar">
          <button 
            className={`nav-btn ${vistaActiva === 'introduccion' ? 'active' : ''}`}
            onClick={() => setVistaActiva('introduccion')}
          >
          Introducción
          </button>
          
          <button 
            className={`nav-btn ${vistaActiva === 'conceptos' ? 'active' : ''}`}
            onClick={() => setVistaActiva('conceptos')}
          >
          Conceptos Fundamentales
          </button>

          <button 
            className={`nav-btn ${vistaActiva === 'simulador' ? 'active' : ''}`}
            onClick={() => setVistaActiva('simulador')}
          >
          Simulador del Sistema
          </button>
        </aside>

        {/* ÁREA DE CONTENIDO DINÁMICO */}
        <div className="content-area">
          
          {vistaActiva === 'introduccion' && (
            <section className="info-box fade-in">
              <h2>Introducción al Aprendizaje por Refuerzo (RL)</h2>
              <p>El Aprendizaje por Refuerzo (Reinforcement Learning) es una rama de la Inteligencia Artificial donde un sistema (llamado agente) aprende a tomar decisiones interactuando con su entorno.</p>
              <p>A diferencia de otras técnicas de IA, el agente aprende mediante <strong>prueba y error</strong>. Si toma una buena decisión, recibe un premio. Si se equivoca, recibe un castigo.</p>
              <p>En esta aplicación interactiva, hemos aplicado este algoritmo para resolver un problema de la vida real: <strong> la detección de anomalías en el tráfico vehicular</strong>. Nuestro agente intentará descubrir cuándo ocurre un accidente basándose en datos de sensores y aprenderá a desviar el tráfico para evitar embotellamientos.</p>
            </section>
          )}

          {vistaActiva === 'conceptos' && (
            <section className="info-box fade-in">
              <h2>Conceptos Fundamentales de RL</h2>
              <p>Para entender el simulador, primero debemos conocer las piezas clave que forman el modelo:</p>
              <ul className="conceptos-lista">
                <li><strong>Agente:</strong> El sistema inteligente. Aquí, es nuestro controlador de desvíos.</li>
                <li><strong>Entorno:</strong> El "espacio" con el que interactúa el agente (la autopista simulada).</li>
                <li><strong>Estado (State):</strong> Lo que detectan los "sensores": <em>Velocidad Promedio</em> y <em>Densidad Vehicular</em>.</li>
                <li><strong>Acción (Action):</strong> Las decisiones que toma el agente: <em>Mantener</em> (Continuar en la via actual) o <em>Desviar</em> (Ocupar ruta alternativa).</li>
                <li><strong>Recompensa (Reward):</strong> El sistema de recompensas para entrenar el agente: Si desvía en un accidente (+10). Si causa embotellamientos (-10). Si activa falsas alarmas (-5).</li>
                <li><strong>Política (Policy):</strong> La "memoria" (Q-Table) que el agente construye para saber qué hacer en el futuro.</li>
              </ul>
            </section>
          )}

          {vistaActiva === 'simulador' && (
            <main className="dashboard fade-in">
              <section className="panel-control">
                <h2>Panel de Control</h2>
                <div className="acciones">
                  <button onClick={entrenarAgente} disabled={entrenando} className="btn-entrenar">
                    {entrenando ? "Entrenando 1000 episodios..." : "1. Entrenar Agente (Cerebro)"}
                  </button>
                  <button onClick={simularPaso} disabled={!qTable} className="btn-simular">
                    2. Simular un paso de tiempo
                  </button>
                </div>
                <div className="mensaje-estado">
                  <strong>Estado:</strong> {mensaje}
                </div>
              </section>

              <section className="panel-simulacion">
                <h2>Monitor de Tráfico</h2>
                {!simulacion ? (
                  <div className="placeholder">Haz clic en "Simular" para inicializar el entorno.</div>
                ) : (
                  <div className="simulador-contenedor">
                    
                    {/* Vista 2D del mapa de calles */}
                    <div className="mapa-2d">
                      <div className="calle-principal"></div>
                      <div className="calle-desvio"></div>
                      
                      {/* Obstáculo/Accidente para simular anomalía */}
                      {simulacion.estado_observado.anomalia_activa && (
                        <div className="obstaculo">💥🚧</div>
                      )}
                      
                      {/* Vehículo con animación dinámica */}
                      <div key={stepId} className={`auto ${claseAnimacionAuto}`}>
                        🚗
                      </div>
                    </div>

                    {/* Datos de sensores y resultados */}
                    <div className="datos-simulacion">
                      <div className="metricas">
                        <p><strong>Velocidad:</strong> {simulacion.estado_observado.velocidad_promedio.toFixed(1)} km/h</p>
                        <p><strong>Densidad:</strong> {simulacion.estado_observado.densidad_trafico.toFixed(1)} %</p>
                        <p><strong>Decisión:</strong> <span className="highlight-accion">{simulacion.accion_tomada}</span></p>
                      </div>
                      
                      <div className="resultado-accion">
                        <p><strong>Recompensa:</strong> <span className={simulacion.recompensa_obtenida > 0 ? "positivo" : "negativo"}>{simulacion.recompensa_obtenida > 0 ? "+" : ""}{simulacion.recompensa_obtenida} puntos</span></p>
                      </div>
                    </div>

                  </div>
                )}
              </section>
            </main>
          )}

        </div>
      </div>
    </div>
  )
}

export default App