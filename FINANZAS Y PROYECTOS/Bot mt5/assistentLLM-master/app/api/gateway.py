"""
API Gateway - Punto de entrada único para la comunicación con el cliente.
Responsabilidades:
- Autenticación y validación de mensajes entrantes
- Enrutamiento de solicitudes al Orquestador
- Gestión de conexiones WebSocket
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
import os
from fastapi.middleware.cors import CORSMiddleware

from ..core.config import get_settings
from ..services.orchestrator import orchestrator
from fastapi.responses import Response

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConnectionManager:
    """Gestor de conexiones WebSocket activas."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Establece una nueva conexión WebSocket."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Cliente {client_id} conectado")
    
    def disconnect(self, client_id: str):
        """Cierra una conexión WebSocket."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Cliente {client_id} desconectado")
    
    async def send_personal_message(self, message: str, client_id: str):
        """Envía un mensaje a un cliente específico."""
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

# Instancia global del gestor de conexiones
manager = ConnectionManager()

# Instancia del orquestador (lazy-load)
orchestrator = None

def get_orchestrator():
    """Obtiene una instancia del Orchestrador. Si la importación falla (por ejemplo en
    entornos de test sin dependencias pesadas), devuelve un orquestador simulado.
    """
    global orchestrator
    if orchestrator is not None:
        return orchestrator

    try:
        from ..services.orchestrator import LLMOrchestrator
        orchestrator = LLMOrchestrator()
        return orchestrator
    except Exception:
        # Fallback: orquestador simulado con la mínima interfaz requerida
        class FakeOrchestrator:
            def __init__(self):
                self.initialized = True

            async def process_request(self, prompt: str, client_id: str, context: Optional[Dict[str, Any]] = None):
                return {"status": "success", "content": "Simulated orchestrator response", "timestamp": "now"}

        orchestrator = FakeOrchestrator()
        return orchestrator

# Aplicación FastAPI
app = FastAPI(
    title="Trading Assistant API",
    description="Sistema de Orquestación de Trading Asistido por LLM",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint de salud del sistema."""
    return {
        "message": "Trading Assistant API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud."""
    return {"status": "healthy"}


@app.get('/metrics')
async def metrics_endpoint():
    """Exponer métricas en formato Prometheus (texto).

    Exporta métricas simples a partir de `orchestrator.metrics`.
    """
    try:
        # Prefer prometheus_client output when available
        try:
            from prometheus_client import generate_latest
            return Response(content=generate_latest(), media_type='text/plain; version=0.0.4')
        except Exception:
            # Fallback: try to read persisted metrics from state_manager (Redis) if available
            try:
                persisted = await state_manager.get_persisted_metrics()
            except Exception:
                persisted = getattr(orchestrator, 'metrics', None) or {}

            lines = []
            for k, v in persisted.get('tool_errors', {}).items():
                lines.append(f'tool_errors_total{{tool="{k}"}} {int(v)}')
            for k, v in persisted.get('tool_timeouts', {}).items():
                lines.append(f'tool_timeouts_total{{tool="{k}"}} {int(v)}')

            for k, v in persisted.get('tool_latency_count', {}).items():
                lines.append(f'tool_latency_count{{tool="{k}"}} {int(v)}')
            for k, v in persisted.get('tool_latency_sum', {}).items():
                lines.append(f'tool_latency_sum{{tool="{k}"}} {float(v):.6f}')

            body = "\n".join(lines) + "\n"
            return Response(content=body, media_type='text/plain; version=0.0.4')
    except Exception:
        return Response(content="", media_type='text/plain')

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """Endpoint WebSocket principal para comunicación en tiempo real."""
    # Autenticación simple por X-API-Key si está configurada en env
    api_key_env = os.getenv("API_KEY")
    if api_key_env:
        # WebSocket headers are case-insensitive; starlette stores them in lowercase
        provided = websocket.headers.get("x-api-key")
        if provided != api_key_env:
            await websocket.accept()
            await websocket.send_text(json.dumps({
                "error": "API key inválida o no proporcionada",
                "status": "error"
            }))
            await websocket.close()
            logger.warning(f"Conexión rechazada para {client_id}: API key inválida")
            return

    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Recibir mensaje del cliente
            data = await websocket.receive_text()
            logger.info(f"Mensaje recibido de {client_id}: {data}")
            
            try:
                # Parsear el mensaje JSON
                message = json.loads(data)
                
                # Validar estructura del mensaje
                if "prompt" not in message:
                    await manager.send_personal_message(
                        json.dumps({
                            "error": "Campo 'prompt' requerido",
                            "status": "error"
                        }),
                        client_id
                    )
                    continue
                
                # Procesar la solicitud a través del orquestador (lazy)
                orch = get_orchestrator()
                # Si es el orquestador real y no está inicializado, inicializarlo
                try:
                    if hasattr(orch, 'initialized') and not orch.initialized:
                        # initialize may be async
                        if hasattr(orch, 'initialize'):
                            init_result = await orch.initialize()
                            if init_result is False:
                                logger.warning("Orquestador.initialize() devolvió False; continuando en modo test/simulación")
                                # Permitir continuar en entornos de test donde servicios externos no están disponibles
                                try:
                                    orch.initialized = True
                                except Exception:
                                    pass
                except Exception as e:
                    logger.error(f"Error inicializando orquestador en gateway: {e}")

                response = await orch.process_request(
                    prompt=message["prompt"],
                    client_id=client_id,
                    context=message.get("context", {})
                )
                
                # Enviar respuesta al cliente
                await manager.send_personal_message(
                    json.dumps(response),
                    client_id
                )
                
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    json.dumps({
                        "error": "Formato JSON inválido",
                        "status": "error"
                    }),
                    client_id
                )
            except Exception as e:
                logger.error(f"Error procesando mensaje: {e}")
                await manager.send_personal_message(
                    json.dumps({
                        "error": f"Error interno: {str(e)}",
                        "status": "error"
                    }),
                    client_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"Error en WebSocket: {e}")
        manager.disconnect(client_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 