"""
Orchestrator - El cerebro central de la aplicación.
Responsabilidades:
- Gestionar el flujo de una solicitud de principio a fin
- Coordinar llamadas entre LLMService, MT5Bridge y StateManager
- Orquestar la ejecución de herramientas
"""

import asyncio
"""
Orchestrator - El cerebro central de la aplicación.
Responsabilidades:
- Gestionar el flujo de una solicitud de principio a fin
- Coordinar llamadas entre LLMService, MT5Bridge y StateManager
- Orquestar la ejecución de herramientas
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
import json
import pandas as pd
from pydantic import BaseModel, ValidationError, Field

from .llm_service import llm_service
from .mt5_bridge import mt5_bridge
from .trading_engine import trading_engine
from .strategy_engine import strategy_engine
from ..core.state_manager import state_manager
from ..services.analysis_tools import run_dynamic_analysis
from ..core.config import get_settings

logger = logging.getLogger(__name__)

# Detectar pandas_ta después de que logger exista
try:
    import pandas_ta as ta
    PANDAS_TA_AVAILABLE = True
except Exception:
    ta = None
    PANDAS_TA_AVAILABLE = False
    logger.warning("pandas_ta no disponible; se usarán rutas fallback para ciertos indicadores")

class LLMOrchestrator:
    """Orquestador principal del sistema."""
    
    def __init__(self):
        self.settings = get_settings()
        self.initialized = False
        self.active_sessions = {}
        # Simple in-memory metrics
        self.metrics = {
            'tool_latencies': {},  # tool_name -> list of latencies (s)
            'tool_timeouts': {},   # tool_name -> count
            'tool_errors': {},     # tool_name -> count
        }

        # Try to initialize prometheus_client metrics if available
        try:
            from prometheus_client import Counter, Histogram
            self._prom_available = True
            self._prom_tool_errors = Counter('tool_errors_total', 'Tool errors', ['tool'])
            self._prom_tool_timeouts = Counter('tool_timeouts_total', 'Tool timeouts', ['tool'])
            # Histogram buckets in seconds
            self._prom_tool_latency = Histogram('tool_latency_seconds', 'Tool latency seconds', ['tool'], buckets=(0.001,0.01,0.05,0.1,0.5,1,2,5,10))
        except Exception:
            self._prom_available = False
            self._prom_tool_errors = None
            self._prom_tool_timeouts = None
            self._prom_tool_latency = None

        # Compensator worker task handle
        self._compensator_worker_task = None
        
    async def initialize(self) -> bool:
        """
        Inicializa el orquestador y todos los servicios dependientes.
        
        Returns:
            bool: True si la inicialización fue exitosa
        """
        try:
            logger.info("Inicializando Orquestador...")
            
            # Inicializar MT5 Bridge
            if not mt5_bridge.initialize():
                logger.error("Error inicializando MT5 Bridge")
                return False
            
            # Inicializar LLM Service
            if not llm_service.initialize():
                logger.error("Error inicializando LLM Service")
                return False

            # Inicializar Trading Engine
            if not await trading_engine.initialize():
                logger.error("Error inicializando Trading Engine")
                return False

            # Inicializar Strategy Engine
            if not await strategy_engine.initialize():
                logger.error("Error inicializando Strategy Engine")
                return False
            
            # Inicializar State Manager
            await state_manager.initialize()
            
            # Configurar herramientas del LLM
            await self._setup_tools()

            # Start compensator worker if enabled in settings
            if getattr(self.settings, 'enable_compensator_worker', False):
                if self._compensator_worker_task is None:
                    self._compensator_worker_task = asyncio.create_task(self._compensator_worker())
            
            self.initialized = True
            logger.info("Orquestador inicializado correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando Orquestador: {e}")
            return False
    
    async def process_request(
        self, 
        prompt: str, 
        client_id: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Procesa una solicitud completa del usuario.
        """
        if not self.initialized:
            return {
                "error": "Sistema no inicializado",
                "status": "error"
            }
        
        try:
            logger.info(f"Procesando solicitud de cliente {client_id}: {prompt[:100]}...")
            
            # Crear o recuperar sesión del cliente
            session = await self._get_or_create_session(client_id)
            
            # Analizar el prompt con el LLM
            analysis_result = await self._analyze_prompt(prompt, context, session)
            
            if analysis_result.get("status") == "error":
                return analysis_result
            
            # Ejecutar herramientas si es necesario
            tool_results = []
            if analysis_result.get("requires_tools", False):
                tool_results = await self._execute_tools(
                    analysis_result.get("tool_calls", []),
                    session
                )

            # If any tool returned an error, propagate an aggregated error response
            if any(r.get("status") == "error" for r in tool_results):
                error_messages = []
                for r in tool_results:
                    if r.get("status") == "error":
                        detail = r.get("result") or {}
                        if isinstance(detail, dict):
                            msg = detail.get("error") or detail.get("details") or str(detail)
                        else:
                            msg = str(detail)
                        error_messages.append(msg)

                summary = error_messages[0] if error_messages else "One or more tools failed or invalid tool calls detected"
                lower_summary = (summary or "").lower()
                if 'argument' not in lower_summary and 'invalid' not in lower_summary and 'argumentos' not in lower_summary:
                    summary = f"Argumentos inválidos: {summary}"
                return {
                    "status": "error",
                    "error": summary,
                    "tool_results": tool_results
                }
            
            # Generar respuesta final
            final_response = await self._generate_final_response(
                prompt, 
                analysis_result, 
                tool_results, 
                session
            )
            
            # Actualizar estado de la sesión
            await self._update_session(session, prompt, final_response)
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error procesando solicitud: {e}")
            return {
                "error": f"Error interno: {str(e)}",
                "status": "error"
            }
    
    async def _get_or_create_session(self, client_id: str) -> Dict[str, Any]:
        """Obtiene o crea una sesión para el cliente."""
        if client_id not in self.active_sessions:
            self.active_sessions[client_id] = {
                "client_id": client_id,
                "created_at": self._get_timestamp(),
                "last_activity": self._get_timestamp(),
                "message_count": 0,
                "context": {}
            }
        
        self.active_sessions[client_id]["last_activity"] = self._get_timestamp()
        self.active_sessions[client_id]["message_count"] += 1
        
        return self.active_sessions[client_id]
    
    async def _analyze_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]], 
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analiza el prompt para determinar qué acciones tomar."""
        try:
            full_context = {
                **session.get("context", {}),
                **(context or {}),
                "session_info": {
                    "message_count": session["message_count"],
                    "session_duration": self._get_session_duration(session)
                }
            }
            
            response = await llm_service.process_prompt(
                prompt=prompt,
                context=full_context,
                use_tools=True
            )
            
            if response.get("status") == "error":
                return response
            
            requires_tools = len(response.get("tool_calls", [])) > 0
            
            return {
                "status": "success",
                "content": response.get("content", ""),
                "tool_calls": response.get("tool_calls", []),
                "requires_tools": requires_tools
            }
            
        except Exception as e:
            logger.error(f"Error analizando prompt: {e}")
            return {
                "error": f"Error analizando prompt: {str(e)}",
                "status": "error"
            }
    
    async def _execute_tools(
        self, 
        tool_calls: List[Dict[str, Any]], 
        session: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Ejecuta las herramientas solicitadas por el LLM."""
        results: List[Dict[str, Any]] = []
        executed_with_compensator: List[Dict[str, Any]] = []

        class ToolCallModel(BaseModel):
            name: str
            args: Dict[str, Any] = Field(default_factory=dict)

        for raw_tool_call in tool_calls:
            try:
                validated = ToolCallModel(**raw_tool_call)
            except ValidationError as ve:
                logger.error(f"Tool call inválido: {ve}")
                results.append({
                    "tool_name": raw_tool_call.get("name", "unknown"),
                    "args": raw_tool_call.get("args", {}),
                    "result": {"error": "Tool call inválido", "details": str(ve)},
                    "status": "error"
                })
                continue

            tool_name = validated.name
            tool_args = validated.args

            logger.info(f"Ejecutando herramienta: {tool_name} con args: {tool_args}")

            timeout = getattr(self.settings, 'max_tool_execution_time', 30)
            try:
                result = await asyncio.wait_for(
                    self._execute_single_tool(tool_name, tool_args, session),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                logger.error(f"Timeout ejecutando herramienta {tool_name} after {timeout}s")
                result = {"error": f"Timeout after {timeout}s", "status": "error"}
            except Exception as e:
                logger.error(f"Error ejecutando herramienta {tool_name}: {e}")
                result = {"error": str(e), "status": "error"}

            results.append({
                "tool_name": tool_name,
                "args": tool_args,
                "result": result,
                "status": "success" if result.get("status") != "error" else "error"
            })

            try:
                from ..tools.registry import get_tool
                te = get_tool(tool_name)
                if te and te.get('meta', {}).get('compensator') and result.get('status') == 'success':
                    executed_with_compensator.append({
                        'tool_name': tool_name,
                        'args': tool_args,
                        'compensator': te.get('meta').get('compensator')
                    })
            except Exception:
                pass
        
        if any(r.get('status') == 'error' for r in results) and executed_with_compensator:
            for entry in reversed(executed_with_compensator):
                comp_name = entry.get('compensator')
                comp_args = {'original_args': entry.get('args', {})}
                try:
                    await self._execute_single_tool(comp_name, comp_args, session)
                except Exception:
                    logger.warning(f"Compensator {comp_name} failed during rollback")

        return results

    async def _execute_single_tool(
        self,
        tool_name: str,
        args: Dict[str, Any],
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Ejecuta una única herramienta."""
        try:
            from ..tools.registry import get_tool

            tool_entry = get_tool(tool_name)
            if tool_entry is None:
                if tool_name == "get_account_info":
                    return await self._tool_get_account_info()
                if tool_name == "get_symbol_info":
                    symbol = args.get("symbol")
                    if not isinstance(symbol, str):
                        return {"error": "Símbolo debe ser una cadena de texto", "status": "error"}
                    return await self._tool_get_symbol_info(symbol)
                if tool_name == "get_historical_data":
                    symbol = args.get("symbol")
                    timeframe = args.get("timeframe")
                    count = args.get("count", 100)
                    if not isinstance(symbol, str) or not isinstance(timeframe, str):
                        return {"error": "Símbolo y timeframe deben ser cadenas de texto", "status": "error"}
                    try:
                        count = int(count)
                    except Exception:
                        count = 100
                    return await self._tool_get_historical_data(symbol, timeframe, count)
                if tool_name == "get_positions":
                    return await self._tool_get_positions()
                if tool_name == "run_dynamic_analysis":
                    symbol = args.get("symbol")
                    timeframe = args.get("timeframe")
                    if not all([symbol, timeframe]):
                        return {"error": "Símbolo y timeframe son requeridos para el análisis", "status": "error"}
                    return await run_dynamic_analysis(symbol, timeframe, args)

                # Execution tools (Phase 4)
                execution_tools = ["open_trade", "close_trade", "modify_trade_protection", "cancel_pending_order"]
                if tool_name in execution_tools:
                    return await trading_engine.handle_direct_tool_call(tool_name, args)

                # Strategy tools (Phase 4)
                if tool_name == "manage_strategy":
                    return await trading_engine.handle_strategy_management(
                        args.get("action"), args
                    )
                if tool_name == "create_and_backtest_strategy":
                    return await trading_engine.handle_strategy_management(
                        "backtest", args
                    )

                return {"error": f"Herramienta '{tool_name}' no implementada", "status": "error"}

            fn = tool_entry.get("run")
            schema = tool_entry.get("schema")
            meta = tool_entry.get("meta") or {}

            requires_confirmation = bool(meta.get("requires_confirmation", False))
            risk_level = str(meta.get("risk_level", "")).lower()

            if requires_confirmation or risk_level == "high":
                if not getattr(self.settings, 'enable_order_execution', False):
                    return {"error": "Order execution is disabled by configuration", "status": "error"}

                confirmed = bool(args.get("confirmed", False)) or (isinstance(session.get("scopes"), list) and "trade:execute" in session.get("scopes"))
                if getattr(self.settings, 'require_double_confirmation', True) and not confirmed:
                    return {"error": "Argumentos inválidos: herramienta de riesgo requiere doble confirmación", "status": "error"}

            if schema is None:
                try:
                    from ..tools.tool_schemas import get_schema
                    schema = get_schema(tool_name)
                except Exception:
                    schema = None

            if schema is not None:
                try:
                    validated = schema(**args)
                    args = validated.dict()
                except Exception as e:
                    return {"error": "Argumentos inválidos para la herramienta", "details": str(e), "status": "error"}

            idempotent = bool(meta.get('idempotent', False))
            max_retries = getattr(self.settings, 'max_tool_retries', 0)
            backoff_base = getattr(self.settings, 'retry_backoff_base', 0.5)

            attempt = 0
            last_err = None
            while True:
                attempt += 1
                start = asyncio.get_event_loop().time()
                try:
                    if asyncio.iscoroutinefunction(fn):
                        result = await fn(args)
                    else:
                        loop = asyncio.get_running_loop()
                        result = await loop.run_in_executor(None, lambda: fn(args))

                    elapsed = asyncio.get_event_loop().time() - start
                    self.metrics['tool_latencies'].setdefault(tool_name, []).append(elapsed)
                    
                    if isinstance(result, dict) and result.get('status') == 'error':
                        self.metrics['tool_errors'][tool_name] = self.metrics['tool_errors'].get(tool_name, 0) + 1
                        last_err = result
                        raise Exception(result.get('error') or 'tool_error')

                    return result

                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    elapsed = asyncio.get_event_loop().time() - start
                    self.metrics['tool_latencies'].setdefault(tool_name, []).append(elapsed)
                    self.metrics['tool_errors'][tool_name] = self.metrics['tool_errors'].get(tool_name, 0) + 1
                    
                    last_err = e
                    if idempotent and attempt <= max_retries:
                        backoff = backoff_base * (2 ** (attempt - 1))
                        await asyncio.sleep(backoff)
                        continue
                    return {"error": str(last_err), "status": "error"}

        except Exception as e:
            logger.error(f"Error ejecutando herramienta {tool_name} via registry: {e}")
            return {"error": str(e), "status": "error"}
    
    def _get_session_duration(self, session: Dict[str, Any]) -> int:
        from datetime import datetime
        created = datetime.fromisoformat(session["created_at"])
        return int((datetime.now() - created).total_seconds())
    
    async def shutdown(self):
        """Cierra el orquestador."""
        mt5_bridge.shutdown()
        await strategy_engine.shutdown()
        await state_manager.shutdown()

# Instancia global
orchestrator = LLMOrchestrator()