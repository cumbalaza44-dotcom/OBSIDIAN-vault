"""
Punto de entrada principal del Sistema de Orquestación de Trading Asistido por LLM.
Responsabilidades:
- Inicializar todos los componentes del sistema
- Configurar y ejecutar el servidor FastAPI
- Manejar el ciclo de vida de la aplicación
"""

import asyncio
import logging
import signal
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.gateway import app as api_app
from app.services.orchestrator import orchestrator
from app.core.config import get_settings, validate_configuration, print_configuration

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('trading_assistant.log') if get_settings().log_file else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor del ciclo de vida de la aplicación.
    """
    # Startup
    logger.info("🚀 Iniciando Trading Assistant...")
    
    # Validar configuración
    if not validate_configuration():
        logger.error("❌ Configuración inválida. Saliendo...")
        sys.exit(1)
    
    # Mostrar configuración
    print_configuration()
    
    # Inicializar orquestador
    if not await orchestrator.initialize():
        logger.error("❌ Error inicializando orquestador. Saliendo...")
        sys.exit(1)
    
    logger.info("✅ Trading Assistant iniciado correctamente")
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando Trading Assistant...")
    await orchestrator.shutdown()
    logger.info("✅ Trading Assistant cerrado correctamente")

def create_app() -> FastAPI:
    """
    Crea la aplicación FastAPI con configuración personalizada.
    
    Returns:
        Aplicación FastAPI configurada
    """
    settings = get_settings()
    
    app = FastAPI(
        title="Trading Assistant API",
        description="Sistema de Orquestación de Trading Asistido por LLM",
        version="1.0.0",
        docs_url="/docs" if settings.api_debug else None,
        redoc_url="/redoc" if settings.api_debug else None,
        lifespan=lifespan
    )
    
    # Incluir rutas del API Gateway
    app.mount("/api", api_app)
    
    # Endpoint de salud
    @app.get("/health")
    async def health_check():
        """Endpoint de verificación de salud del sistema."""
        return {
            "status": "healthy",
            "service": "Trading Assistant",
            "version": "1.0.0"
        }
    
    # Endpoint de métricas
    @app.get("/metrics")
    async def get_metrics():
        """Endpoint para obtener métricas del sistema."""
        from app.core.state_manager import state_manager
        return await state_manager.get_system_metrics()
    
    return app

def signal_handler(signum, frame):
    """
    Manejador de señales para cierre graceful.
    """
    logger.info(f"Recibida señal {signum}. Cerrando aplicación...")
    sys.exit(0)

async def main():
    """
    Función principal asíncrona.
    """
    settings = get_settings()
    
    # Configurar manejadores de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Crear aplicación
    app = create_app()
    
    # Configurar servidor
    config = uvicorn.Config(
        app=app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
        reload=settings.api_debug,
        access_log=True
    )
    
    # Crear y ejecutar servidor
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Aplicación interrumpida por el usuario")
    except Exception as e:
        logger.error(f"Error ejecutando aplicación: {e}")
        sys.exit(1) 