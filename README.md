# Sistema Inteligente de Gestión de Tráfico con Aprendizaje por Refuerzo

Este proyecto es una aplicación web interactiva desarrollada para demostrar el uso del **Aprendizaje por Refuerzo (Reinforcement Learning)** en la detección y gestión de anomalías. Específicamente, simula un entorno de tráfico vehicular donde un agente inteligente aprende a detectar accidentes (anomalías) y desviar el tráfico para evitar embotellamientos.

## Características Principales
* **Backend:** Desarrollado en Python con FastAPI. Implementa un agente de Q-Learning desde cero.
* **Frontend:** Desarrollado en React y Vite. Incluye una sección teórica, un panel de control interactivo y una simulación 2D dinámica del comportamiento del agente.
* **Modelo RL:** El agente observa el estado (Velocidad Promedio y Densidad de Tráfico) y toma decisiones (Mantener vía o Desviar) maximizando las recompensas a lo largo del tiempo.

## Requisitos Previos

Para ejecutar este proyecto en un entorno local, es necesario tener instalado:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (o Docker y Docker Compose en Linux).

## Instalación y Ejecución (Vía Docker)

**1. Abrir la terminal y navegar a la raiz del proyecto (si no se encuentra ahí)**
    
    cd Proyecto_Reinforcement_Learning

**2. Ejecuta el siguiente comando para construir las imágenes y levantar los contenedores:**
    
    docker-compose up --build


## ¿Cómo usar la aplicación?
1. Abre tu navegador web y dirígete a http://localhost:5173.
2. Lee las secciones de Introducción y Conceptos Fundamentales para entender el contexto del problema.
3. Ve a la sección Simulador del Sistema.
4. Presiona el botón "1. Entrenar Agente (Cerebro)". Espera unos segundos hasta que el sistema indique que el entrenamiento fue exitoso.
5. Presiona "2. Simular un paso de tiempo" repetidas veces para ver cómo el agente interactúa con el entorno 2D y toma decisiones en tiempo real ante el tráfico normal o los accidentes.