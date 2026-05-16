"""
StateManager - Gestión de estado del sistema.
Responsabilidades:
- Mantener el estado de la sesión
- Gestionar operaciones abiertas y contexto de conversación
- Proporcionar persistencia y consistencia de datos
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
import json

from .config import get_settings

logger = logging.getLogger(__name__)

# Tipo para Redis client
try:
    import redis.asyncio as redis
    RedisClient = redis.Redis
except ImportError:
    RedisClient = Any  # Fallback si Redis no está disponible

class StateManager:
    """Gestor de estado del sistema."""
    
    def __init__(self):
        self.settings = get_settings()
        self.initialized = False
        
        # Estado en memoria (por defecto)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.operations: Dict[str, Dict[str, Any]] = {}
        # Trades en memoria
        self.trades: Dict[str, Dict[str, Any]] = {}
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.system_metrics: Dict[str, Any] = {}
        # Compensator queue (in-memory fallback)
        self._compensator_queue: List[Dict[str, Any]] = []

        # Redis client (opcional)
        self.redis_client: Optional[RedisClient] = None
        
    async def initialize(self) -> bool:
        """
        Inicializa el gestor de estado.
        
        Returns:
            bool: True si la inicialización fue exitosa
        """
        try:
            logger.info("Inicializando State Manager...")
            
            # Inicializar Redis si está configurado
            if self.settings.state_backend == "redis":
                await self._initialize_redis()
            
            # Inicializar métricas del sistema
            self.system_metrics = {
                "startup_time": datetime.now().isoformat(),
                "total_sessions": 0,
                "active_sessions": 0,
                "total_operations": 0,
                "total_messages": 0
            }
            
            self.initialized = True
            logger.info("State Manager inicializado correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando State Manager: {e}")
            return False
    
    async def _initialize_redis(self):
        """Inicializa la conexión con Redis."""
        try:
            # Intentar importar redis.asyncio (versión 4.2+)
            try:
                import redis.asyncio as redis
                redis_client_class = redis.Redis
            except ImportError:
                # Fallback para versiones anteriores
                import redis
                if not hasattr(redis, 'from_url'):
                    raise ImportError("Versión de Redis incompatible")
                redis_client_class = redis.Redis
            
            if not self.settings.redis_url:
                logger.warning("Redis configurado pero REDIS_URL no especificada")
                return
            
            self.redis_client = redis_client_class.from_url(self.settings.redis_url)
            await self.redis_client.ping()
            logger.info("Conexión con Redis establecida")
            
        except ImportError:
            logger.error("Redis no está instalado. Usando almacenamiento en memoria")
            self.redis_client = None
        except Exception as e:
            logger.error(f"Error conectando con Redis: {e}")
            self.redis_client = None
    
    async def create_session(self, client_id: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Crea una nueva sesión para un cliente.
        
        Args:
            client_id: ID del cliente
            metadata: Metadatos adicionales de la sesión
            
        Returns:
            Sesión creada
        """
        session = {
            "client_id": client_id,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "status": "active",
            "message_count": 0,
            "metadata": metadata or {},
            "context": {}
        }
        
        # Guardar en memoria
        self.sessions[client_id] = session
        
        # Guardar en Redis si está disponible
        if self.redis_client:
            await self.redis_client.setex(
                f"session:{client_id}",
                3600,  # TTL de 1 hora
                json.dumps(session)
            )
        
        # Actualizar métricas
        self.system_metrics["total_sessions"] += 1
        self.system_metrics["active_sessions"] += 1
        
        logger.info(f"Sesión creada para cliente {client_id}")
        return session
    
    async def get_session(self, client_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una sesión existente.
        
        Args:
            client_id: ID del cliente
            
        Returns:
            Sesión o None si no existe
        """
        # Buscar en memoria primero
        if client_id in self.sessions:
            return self.sessions[client_id]
        
        # Buscar en Redis si está disponible
        if self.redis_client:
            try:
                data = await self.redis_client.get(f"session:{client_id}")
                if data:
                    session = json.loads(data)
                    self.sessions[client_id] = session  # Cache en memoria
                    return session
            except Exception as e:
                logger.error(f"Error obteniendo sesión de Redis: {e}")
        
        return None
    
    async def update_session(self, client_id: str, updates: Dict[str, Any]) -> bool:
        """
        Actualiza una sesión existente.
        
        Args:
            client_id: ID del cliente
            updates: Actualizaciones a aplicar
            
        Returns:
            True si la actualización fue exitosa
        """
        session = await self.get_session(client_id)
        if not session:
            return False
        
        # Aplicar actualizaciones
        session.update(updates)
        session["last_activity"] = datetime.now().isoformat()
        
        # Guardar en memoria
        self.sessions[client_id] = session
        
        # Guardar en Redis si está disponible
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    f"session:{client_id}",
                    3600,  # TTL de 1 hora
                    json.dumps(session)
                )
            except Exception as e:
                logger.error(f"Error guardando sesión en Redis: {e}")
        
        return True
    
    async def close_session(self, client_id: str) -> bool:
        """
        Cierra una sesión.
        
        Args:
            client_id: ID del cliente
            
        Returns:
            True si el cierre fue exitoso
        """
        session = await self.get_session(client_id)
        if not session:
            return False
        
        # Marcar como cerrada
        session["status"] = "closed"
        session["closed_at"] = datetime.now().isoformat()
        
        # Guardar cambios
        await self.update_session(client_id, session)
        
        # Actualizar métricas
        self.system_metrics["active_sessions"] = max(0, self.system_metrics["active_sessions"] - 1)
        
        logger.info(f"Sesión cerrada para cliente {client_id}")
        return True
    
    async def add_message(self, client_id: str, message: Dict[str, Any]) -> bool:
        """
        Agrega un mensaje al historial de conversación.
        
        Args:
            client_id: ID del cliente
            message: Mensaje a agregar
            
        Returns:
            True si se agregó correctamente
        """
        if client_id not in self.conversations:
            self.conversations[client_id] = []
        
        # Agregar timestamp si no existe
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().isoformat()
        
        # Agregar a la lista
        self.conversations[client_id].append(message)
        
        # Limitar el tamaño del historial
        max_history = self.settings.max_conversation_history
        if len(self.conversations[client_id]) > max_history:
            self.conversations[client_id] = self.conversations[client_id][-max_history:]
        
        # Guardar en Redis si está disponible
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    f"conversation:{client_id}",
                    7200,  # TTL de 2 horas
                    json.dumps(self.conversations[client_id])
                )
            except Exception as e:
                logger.error(f"Error guardando conversación en Redis: {e}")
        
        # Actualizar métricas
        self.system_metrics["total_messages"] += 1
        
        return True
    
    async def get_conversation_history(self, client_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de conversación de un cliente.
        
        Args:
            client_id: ID del cliente
            limit: Número máximo de mensajes a retornar
            
        Returns:
            Lista de mensajes
        """
        # Buscar en memoria
        if client_id in self.conversations:
            history = self.conversations[client_id]
        else:
            # Buscar en Redis si está disponible
            if self.redis_client:
                try:
                    data = await self.redis_client.get(f"conversation:{client_id}")
                    if data:
                        history = json.loads(data)
                        self.conversations[client_id] = history  # Cache en memoria
                    else:
                        history = []
                except Exception as e:
                    logger.error(f"Error obteniendo conversación de Redis: {e}")
                    history = []
            else:
                history = []
        
        # Aplicar límite si se especifica
        if limit:
            history = history[-limit:]
        
        return history
    
    async def add_operation(self, operation_id: str, operation_data: Dict[str, Any]) -> bool:
        """
        Agrega una operación al estado del sistema.
        
        Args:
            operation_id: ID de la operación
            operation_data: Datos de la operación
            
        Returns:
            True si se agregó correctamente
        """
        operation = {
            "operation_id": operation_id,
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            **operation_data
        }
        
        self.operations[operation_id] = operation
        
        # Guardar en Redis si está disponible
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    f"operation:{operation_id}",
                    1800,  # TTL de 30 minutos
                    json.dumps(operation)
                )
            except Exception as e:
                logger.error(f"Error guardando operación en Redis: {e}")
        
        # Actualizar métricas
        self.system_metrics["total_operations"] += 1
        
        return True

    # --- Compensator queue helpers ---
    async def push_compensator_task(self, task: Dict[str, Any]) -> bool:
        """
        Encola una tarea de compensación. Si Redis está activo, la persiste en lista 'compensators'.
        """
        try:
            serialized = json.dumps(task)
            if self.redis_client:
                await self.redis_client.rpush('compensators', serialized)
            else:
                self._compensator_queue.append(task)
            return True
        except Exception as e:
            logger.error(f"Error encolando compensator task: {e}")
            return False

    async def pop_compensator_task(self) -> Optional[Dict[str, Any]]:
        """
        Extrae una tarea de la cola de compensadores (FIFO). Retorna None si no hay tareas.
        """
        try:
            if self.redis_client:
                item = await self.redis_client.lpop('compensators')
                if item:
                    return json.loads(item)
                return None
            else:
                if self._compensator_queue:
                    return self._compensator_queue.pop(0)
                return None
        except Exception as e:
            logger.error(f"Error extrayendo compensator task: {e}")
            return None

    async def pop_compensator_task_blocking(self, timeout: int = 5) -> Optional[Dict[str, Any]]:
        """
        Blocking pop that moves the item to a processing list (compensators_processing) using BRPOPLPUSH.
        Returns the deserialized task or None on timeout. Falls back to non-blocking pop if Redis not available.
        """
        try:
            if self.redis_client:
                item = await self.redis_client.brpoplpush('compensators', 'compensators_processing', timeout=timeout)
                if item:
                    return json.loads(item)
                return None
            else:
                # fallback: non-blocking pop
                return await self.pop_compensator_task()
        except Exception as e:
            logger.error(f"Error extrayendo compensator task (blocking): {e}")
            return None

    async def mark_compensator_done(self, task: Dict[str, Any]) -> bool:
        """
        Remove a task from the compensators_processing list after successful processing.
        """
        try:
            serialized = json.dumps(task)
            if self.redis_client:
                await self.redis_client.lrem('compensators_processing', 1, serialized)
            else:
                # no-op for in-memory (it was popped already)
                pass
            return True
        except Exception as e:
            logger.error(f"Error marcando compensator done: {e}")
            return False

    async def requeue_processing_to_main(self) -> None:
        """
        At startup, move any tasks left in 'compensators_processing' back to 'compensators' to ensure they will be retried.
        """
        try:
            if self.redis_client:
                while True:
                    item = await self.redis_client.lpop('compensators_processing')
                    if not item:
                        break
                    await self.redis_client.rpush('compensators', item)
            else:
                # nothing to do for in-memory queue
                pass
        except Exception as e:
            logger.error(f"Error requeueing processing tasks: {e}")

    # --- Metrics persistence helpers ---
    async def incr_tool_error(self, tool: str, amount: int = 1):
        try:
            # in-memory
            self.system_metrics.setdefault('tool_errors', {})
            self.system_metrics['tool_errors'][tool] = self.system_metrics['tool_errors'].get(tool, 0) + amount
            if self.redis_client:
                await self.redis_client.hincrby('metrics:tool_errors', tool, amount)
        except Exception as e:
            logger.error(f"Error incrementing tool error metric: {e}")

    async def incr_tool_timeout(self, tool: str, amount: int = 1):
        try:
            self.system_metrics.setdefault('tool_timeouts', {})
            self.system_metrics['tool_timeouts'][tool] = self.system_metrics['tool_timeouts'].get(tool, 0) + amount
            if self.redis_client:
                await self.redis_client.hincrby('metrics:tool_timeouts', tool, amount)
        except Exception as e:
            logger.error(f"Error incrementing tool timeout metric: {e}")

    async def add_tool_latency(self, tool: str, latency: float):
        try:
            self.system_metrics.setdefault('tool_latencies', {})
            self.system_metrics['tool_latencies'].setdefault(tool, []).append(latency)
            if self.redis_client:
                # store count and sum in hashes
                await self.redis_client.hincrby('metrics:tool_latency_count', tool, 1)
                await self.redis_client.hincrbyfloat('metrics:tool_latency_sum', tool, float(latency))
        except Exception as e:
            logger.error(f"Error adding tool latency metric: {e}")

    async def get_persisted_metrics(self) -> Dict[str, Any]:
        """Return a dictionary with persisted metrics read from Redis if available, else from memory snapshot."""
        try:
            if self.redis_client:
                errors = await self.redis_client.hgetall('metrics:tool_errors')
                timeouts = await self.redis_client.hgetall('metrics:tool_timeouts')
                counts = await self.redis_client.hgetall('metrics:tool_latency_count')
                sums = await self.redis_client.hgetall('metrics:tool_latency_sum')

                # decode bytes to strings if necessary
                def decode_map(m):
                    return {k.decode() if isinstance(k, bytes) else k: float(v.decode() if isinstance(v, bytes) else v) for k,v in (m.items() if isinstance(m, dict) else m.items())}

                return {
                    'tool_errors': decode_map(errors),
                    'tool_timeouts': decode_map(timeouts),
                    'tool_latency_count': decode_map(counts),
                    'tool_latency_sum': decode_map(sums)
                }
            else:
                return {
                    'tool_errors': self.system_metrics.get('tool_errors', {}),
                    'tool_timeouts': self.system_metrics.get('tool_timeouts', {}),
                    'tool_latency_count': {k: len(v) for k,v in self.system_metrics.get('tool_latencies', {}).items()},
                    'tool_latency_sum': {k: sum(v) for k,v in self.system_metrics.get('tool_latencies', {}).items()}
                }
        except Exception as e:
            logger.error(f"Error getting persisted metrics: {e}")
            return {}

    # --- Trade helper methods (Etapa 3 helpers) ---
    async def add_trade(self, trade_id: str, trade_data: Dict[str, Any]) -> bool:
        """
        Agrega un trade (operación ejecutada o planeada) al estado.
        """
        trade = {
            "trade_id": trade_id,
            "created_at": datetime.now().isoformat(),
            "status": trade_data.get("status", "open"),
            **trade_data
        }

        self.trades[trade_id] = trade

        if self.redis_client:
            try:
                await self.redis_client.setex(
                    f"trade:{trade_id}",
                    3600,
                    json.dumps(trade)
                )
            except Exception as e:
                logger.error(f"Error guardando trade en Redis: {e}")

        return True

    async def update_trade(self, trade_id: str, updates: Dict[str, Any]) -> bool:
        """
        Actualiza un trade existente.
        """
        if trade_id not in self.trades:
            return False

        self.trades[trade_id].update(updates)
        self.trades[trade_id]["updated_at"] = datetime.now().isoformat()

        if self.redis_client:
            try:
                await self.redis_client.setex(
                    f"trade:{trade_id}",
                    3600,
                    json.dumps(self.trades[trade_id])
                )
            except Exception as e:
                logger.error(f"Error actualizando trade en Redis: {e}")

        return True

    async def get_trade(self, trade_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un trade por su ID."""
        if trade_id in self.trades:
            return self.trades[trade_id]

        if self.redis_client:
            try:
                data = await self.redis_client.get(f"trade:{trade_id}")
                if data:
                    trade = json.loads(data)
                    self.trades[trade_id] = trade
                    return trade
            except Exception as e:
                logger.error(f"Error obteniendo trade de Redis: {e}")

        return None

    async def list_trades(self) -> List[Dict[str, Any]]:
        """Lista todos los trades en memoria (no paginado)."""
        return list(self.trades.values())

    async def get_state(self) -> Dict[str, Any]:
        """Devuelve un snapshot del estado relevante (sesiones, operaciones, trades, métricas)."""
        return {
            "sessions": list(self.sessions.keys()),
            "operations_count": len(self.operations),
            "trades_count": len(self.trades),
            "system_metrics": self.system_metrics
        }
    
    async def update_operation(self, operation_id: str, updates: Dict[str, Any]) -> bool:
        """
        Actualiza una operación existente.
        
        Args:
            operation_id: ID de la operación
            updates: Actualizaciones a aplicar
            
        Returns:
            True si la actualización fue exitosa
        """
        if operation_id not in self.operations:
            return False
        
        self.operations[operation_id].update(updates)
        self.operations[operation_id]["updated_at"] = datetime.now().isoformat()
        
        # Guardar en Redis si está disponible
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    f"operation:{operation_id}",
                    1800,  # TTL de 30 minutos
                    json.dumps(self.operations[operation_id])
                )
            except Exception as e:
                logger.error(f"Error actualizando operación en Redis: {e}")
        
        return True
    
    async def get_operation(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene una operación específica.
        
        Args:
            operation_id: ID de la operación
            
        Returns:
            Operación o None si no existe
        """
        if operation_id in self.operations:
            return self.operations[operation_id]
        
        # Buscar en Redis si está disponible
        if self.redis_client:
            try:
                data = await self.redis_client.get(f"operation:{operation_id}")
                if data:
                    operation = json.loads(data)
                    self.operations[operation_id] = operation  # Cache en memoria
                    return operation
            except Exception as e:
                logger.error(f"Error obteniendo operación de Redis: {e}")
        
        return None
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """
        Obtiene las métricas del sistema.
        
        Returns:
            Métricas del sistema
        """
        metrics = self.system_metrics.copy()
        metrics["current_time"] = datetime.now().isoformat()
        metrics["uptime"] = self._calculate_uptime()
        return metrics
    
    def _calculate_uptime(self) -> str:
        """Calcula el tiempo de actividad del sistema."""
        try:
            startup_time = datetime.fromisoformat(self.system_metrics["startup_time"])
            uptime = datetime.now() - startup_time
            return str(uptime).split('.')[0]  # Sin microsegundos
        except:
            return "Unknown"
    
    async def cleanup_expired_sessions(self):
        """Limpia sesiones expiradas."""
        current_time = datetime.now()
        expired_sessions = []
        
        for client_id, session in self.sessions.items():
            last_activity = datetime.fromisoformat(session["last_activity"])
            if current_time - last_activity > timedelta(hours=1):
                expired_sessions.append(client_id)
        
        for client_id in expired_sessions:
            await self.close_session(client_id)
            logger.info(f"Sesión expirada limpiada: {client_id}")
    
    async def shutdown(self):
        """Cierra el gestor de estado."""
        try:
            logger.info("Cerrando State Manager...")
            
            # Cerrar conexión con Redis
            if self.redis_client:
                await self.redis_client.close()
            
            # Limpiar datos en memoria
            self.sessions.clear()
            self.operations.clear()
            self.conversations.clear()
            
            logger.info("State Manager cerrado correctamente")
            
        except Exception as e:
            logger.error(f"Error cerrando State Manager: {e}")

# Instancia global del gestor de estado
state_manager = StateManager() 