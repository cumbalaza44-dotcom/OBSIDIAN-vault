import asyncio
import logging
import sys
import os

# Añadir el directorio raíz al path para poder importar app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.orchestrator import orchestrator
from app.services.mt5_bridge import mt5_bridge

async def test_init():
    logging.basicConfig(level=logging.INFO)
    print("DEBUG: Entrando en test_init")
    print("Iniciando prueba de inicialización del Orquestador (MODO SIMULADO)...")
    mt5_bridge.simulated = True
    success = await orchestrator.initialize()
    if success:
        print("¡ÉXITO! El Orquestador se inicializó correctamente con TradingEngine.")
    else:
        print("ERROR: Falló la inicialización del Orquestador.")
    
    await orchestrator.shutdown()

if __name__ == "__main__":
    asyncio.run(test_init())
