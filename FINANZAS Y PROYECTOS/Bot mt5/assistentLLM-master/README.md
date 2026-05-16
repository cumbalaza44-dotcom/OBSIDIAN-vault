# Trading Assistant - Sistema de Orquestación de Trading Asistido por LLM

## Descripción

Sistema de trading algorítmico avanzado que utiliza un Modelo de Lenguaje Grande (LLM) para interpretar comandos en lenguaje natural y ejecutar acciones de trading y análisis a través de un puente de baja latencia con MetaTrader 5.

## Características

- 🤖 **Asistente de IA**: Integración con Google Gemini para interpretación de comandos naturales
- 📊 **Análisis de Mercado**: Herramientas avanzadas de análisis técnico y fundamental
- ⚡ **Baja Latencia**: Comunicación optimizada con MetaTrader 5
- 🔄 **Arquitectura Modular**: Servicios desacoplados para máxima flexibilidad
- 🌐 **API WebSocket**: Comunicación en tiempo real con clientes
- 📈 **Gestión de Estado**: Sistema robusto de gestión de sesiones y operaciones

## Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente UI    │    │   Google AI     │    │   MetaTrader 5  │
│   (WebSocket)   │    │   (Gemini)      │    │   Terminal      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   API Gateway   │
                    │   (FastAPI)     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Orchestrator   │
                    │   (Cerebro)     │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  LLM Service    │    │  MT5 Bridge     │    │ State Manager   │
│  (Google AI)    │    │  (MetaTrader)   │    │  (Estado)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Instalación

### Prerrequisitos

- Python 3.8 o superior
- MetaTrader 5 terminal instalado
- Cuenta de Google AI (para Gemini)

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd trading_assistant
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# Google AI Configuration
GOOGLE_API_KEY=tu_api_key_de_google_ai

# MT5 Configuration (opcional)
MT5_LOGIN=tu_login_mt5
MT5_PASSWORD=tu_password_mt5
MT5_SERVER=tu_servidor_mt5

# Logging
LOG_LEVEL=INFO
LOG_FILE=trading_assistant.log

# State Backend
STATE_BACKEND=memory  # memory o redis
REDIS_URL=redis://localhost:6379  # solo si usas redis
```

### 5. Verificar instalación

```bash
python main.py
```

## Uso

### Iniciar el servidor

```bash
python main.py
```

El servidor estará disponible en `http://localhost:8000`

### Endpoints disponibles

- **Health Check**: `GET /health`
- **Métricas**: `GET /metrics`
- **Documentación API**: `GET /docs` (solo en modo debug)
- **WebSocket**: `WS /api/ws/{client_id}`

### Ejemplo de uso con WebSocket

```python
import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://localhost:8000/api/ws/test_client"
    
    async with websockets.connect(uri) as websocket:
        # Enviar mensaje
        message = {
            "prompt": "¿Cuál es el estado de mi cuenta de trading?",
            "context": {}
        }
        
        await websocket.send(json.dumps(message))
        
        # Recibir respuesta
        response = await websocket.recv()
        print(f"Respuesta: {response}")

# Ejecutar
asyncio.run(test_connection())
```

## Estructura del Proyecto

```
trading_assistant/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── gateway.py          # API Gateway con WebSockets
│   ├── services/
│   │   ├── __init__.py
│   │   ├── mt5_bridge.py       # Puente con MetaTrader 5
│   │   ├── llm_service.py      # Servicio de Google AI
│   │   └── orchestrator.py     # Orquestador principal
│   ├── tools/
│   │   └── __init__.py         # Herramientas del LLM
│   └── core/
│       ├── __init__.py
│       ├── config.py           # Configuración del sistema
│       └── state_manager.py    # Gestión de estado
├── main.py                     # Punto de entrada
├── requirements.txt            # Dependencias
├── .env                        # Variables de entorno
└── README.md                   # Este archivo
```

## Desarrollo

### Plan de Implementación

El desarrollo se realiza en 4 etapas:

1. **Etapa 1: Conexión** (0% - 20%)
   - ✅ Estructura del proyecto
   - 🔄 API Gateway básico
   - 🔄 MT5 Bridge básico
   - 🔄 LLM Service básico

2. **Etapa 2: Datos** (20% - 50%)
   - 🔄 DataEngine optimizado
   - 🔄 Herramientas de análisis
   - 🔄 Procesamiento de datos históricos

3. **Etapa 3: Cerebro** (50% - 80%)
   - 🔄 Orquestador completo
   - 🔄 Integración LLM
   - 🔄 Gestión de estado avanzada

4. **Etapa 4: Ejecución** (80% - 100%)
   - 🔄 Herramientas de trading
   - 🔄 Motor de estrategias
   - 🔄 Control total del sistema

### Ejecutar tests

```bash
pytest tests/
```

### Modo desarrollo

```bash
# Activar modo debug
export API_DEBUG=true
python main.py
```

## Configuración Avanzada

### Redis (Opcional)

Para usar Redis como backend de estado:

1. Instalar Redis
2. Configurar `STATE_BACKEND=redis` en `.env`
3. Configurar `REDIS_URL` en `.env`

### Logging

Configurar logging en `.env`:

```env
LOG_LEVEL=DEBUG
LOG_FILE=trading_assistant.log
```

### Seguridad

En producción:

1. Configurar `API_DEBUG=false`
2. Restringir `CORS_ORIGINS`
3. Usar HTTPS
4. Implementar autenticación

## Troubleshooting

### Error: MetaTrader5 no disponible

```bash
# Instalar MetaTrader5
pip install MetaTrader5
```

### Error: Google AI no disponible

```bash
# Instalar Google AI
pip install google-generativeai
```

### Error: Puerto ocupado

Cambiar puerto en `.env`:

```env
API_PORT=8001
```

## Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas:

- Crear un issue en GitHub
- Contactar al equipo de desarrollo
- Revisar la documentación en `/docs`

---

**Nota**: Este sistema está diseñado para uso educativo y de desarrollo. Úselo en producción bajo su propia responsabilidad y asegúrese de cumplir con todas las regulaciones financieras aplicables. 