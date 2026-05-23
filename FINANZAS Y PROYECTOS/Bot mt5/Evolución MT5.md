- [x] Estudiar migración de trading assistant 📅 2026-05-16 ✅ 2026-05-23
- [ ] Estudiar, funcionamiento y o propuestas de funcionamiento para luego hacer la migración con N8N o alguna otra plataforma de más rápido, desarrollo y producción para hoy
- [x] Recordatorio de prueba 📅 2026-05-16 ✅ 2026-05-16
- [x]  🔼 📅 2026-05-16 ✅ 2026-05-16
- [ ] Ciclo de trabajo 🔁 every day 📅 2026-05-20
- [x] Ciclo de trabajo 🔁 every day 📅 2026-05-19 ✅ 2026-05-23
- [x] Ciclo de trabajo 🔁 every day 📅 2026-05-18 ✅ 2026-05-23
- [x] Ciclo de trabajo 🔁 every day 📅 2026-05-17 ✅ 2026-05-23

## Características de funcionamiento 
- low account
- Bajo flotante 
- Operaciones inteligentes 
- Rendimiento seguro aceptable
- determinar cuáles son las formas de construcción que nos permitan más herramientas de usuario
- Motor de estrategia 
## métodos de operación 
- señal 
- Cobertura 
- Cerrar 
## arquitectura 
graph TD
    subgraph "Usuario"
        A[UI - Interfaz de Usuario]
    end

    subgraph "Núcleo / Cerebro del Sistema"
        B(Orquestador Central)
        C[Toolbox - Caja de Herramientas]
        D[StateManager - Gestor de Estado]
        E[LLMService - Servicio del LLM]
    end

    subgraph "Servicios Externos"
        F[API de Deriv]
        G[API del LLM]
    end
    
    subgraph "Módulos Periféricos"
        H[APIManager - Gestor de Conexión]
    end

    A -- "Evento: OnUserQuery" --> B
    B -- 1. Coordina --> E
    E -- 2. Llama --> G
    G -- 3. Respuesta --> E
    B -- 4. Ejecuta Herramienta --> C
    C -- 5. Consulta Estado --> D
    C -- 6. Ejecuta Acción --> H
    H -- 7. Llama --> F
    F -- 8. Resultado --> H
    H -- "Evento: OnDataReceived" --> B
    B -- 9. Actualiza Estado --> D
    B -- 10
U

## plan de desarrollo 
Que formas de construcción nos permiten un desarrollo de más herramientas para el usuario 
