"""
StrategyEngine - Motor de estrategias autónomas con arquitectura OOP.
Responsabilidades:
- Gestionar estrategias activas (activate/deactivate)
- Evaluar señales de trading en tiempo real
- Ejecutar backtesting rápido de estrategias
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from datetime import datetime
import json

logger = logging.getLogger(__name__)

# ============================================================================
# CLASE BASE ABSTRACTA
# ============================================================================

class Strategy(ABC):
    """Clase base abstracta para todas las estrategias."""
    
    def __init__(self, name: str, symbol: str, timeframe: str):
        self.name = name
        self.symbol = symbol
        self.timeframe = timeframe
        self.id = f"{name}_{symbol}_{timeframe}_{int(datetime.now().timestamp())}"
        self.status = "stopped"
        self.created_at = datetime.now().isoformat()
        self.trades = []
        self.last_evaluation = None

    @abstractmethod
    async def check_conditions(self, data: Any = None) -> Optional[Dict[str, Any]]:
        """
        Evalúa las condiciones de la estrategia.
        
        Args:
            data: DataFrame con datos históricos (opcional)
        
        Returns:
            Dict con señal de trading o None si no hay señal
            Formato: {"action": "buy"/"sell", "volume": 0.1, "sl_pips": 20, "tp_pips": 40}
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Retorna el nombre de la estrategia."""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Devuelve información de la estrategia."""
        return {
            "id": self.id,
            "name": self.name,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "status": self.status,
            "created_at": self.created_at,
            "total_trades": len(self.trades),
            "last_evaluation": self.last_evaluation
        }

# ============================================================================
# ESTRATEGIAS CONCRETAS
# ============================================================================

class StrategyEMACross(Strategy):
    """Estrategia de cruce de medias móviles exponenciales."""
    
    def __init__(self, symbol: str, timeframe: str, fast_period: int = 10, slow_period: int = 20):
        super().__init__("EMACross", symbol, timeframe)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.last_signal = None

    def get_name(self) -> str:
        return f"EMACross_{self.fast_period}_{self.slow_period}"

    async def check_conditions(self, data: Any = None) -> Optional[Dict[str, Any]]:
        """
        Evalúa cruce de EMAs.
        Señal de compra: EMA rápida cruza por encima de EMA lenta
        Señal de venta: EMA rápida cruza por debajo de EMA lenta
        """
        try:
            from .mt5_bridge import mt5_bridge
            from .data_engine import data_engine
            
            # Obtener datos históricos si no se proporcionan
            if data is None:
                timeframe_map = {"M1": 1, "M5": 5, "M15": 15, "M30": 30, "H1": 16385, "H4": 16388, "D1": 16408}
                mt5_tf = timeframe_map.get(self.timeframe.upper(), 16385)
                
                from datetime import datetime, timedelta
                end_date = datetime.now()
                start_date = end_date - timedelta(days=5)
                
                data = mt5_bridge.get_historical_data(
                    self.symbol, mt5_tf, start_date, end_date, as_polars=True
                )
            
            if data is None or len(data) < self.slow_period + 2:
                return None
            
            # Calcular EMAs
            ema_fast = data_engine.calculate_ema(data, self.fast_period)
            ema_slow = data_engine.calculate_ema(data, self.slow_period)
            
            if ema_fast is None or ema_slow is None:
                return None
            
            # Detectar cruce
            current_fast = ema_fast[-1]
            current_slow = ema_slow[-1]
            prev_fast = ema_fast[-2]
            prev_slow = ema_slow[-2]
            
            signal = None
            
            # Cruce alcista
            if prev_fast <= prev_slow and current_fast > current_slow:
                if self.last_signal != "buy":
                    signal = {
                        "action": "buy",
                        "volume": 0.01,
                        "sl_pips": 50,
                        "tp_pips": 100,
                        "comment": f"{self.get_name()} - Bullish Cross"
                    }
                    self.last_signal = "buy"
            
            # Cruce bajista
            elif prev_fast >= prev_slow and current_fast < current_slow:
                if self.last_signal != "sell":
                    signal = {
                        "action": "sell",
                        "volume": 0.01,
                        "sl_pips": 50,
                        "tp_pips": 100,
                        "comment": f"{self.get_name()} - Bearish Cross"
                    }
                    self.last_signal = "sell"
            
            self.last_evaluation = datetime.now().isoformat()
            return signal
            
        except Exception as e:
            logger.error(f"Error en StrategyEMACross.check_conditions: {e}")
            return None


class DynamicStrategy(Strategy):
    """Estrategia definida dinámicamente por reglas JSON."""
    
    def __init__(self, name: str, symbol: str, timeframe: str, rules: Dict[str, Any]):
        super().__init__(name, symbol, timeframe)
        self.rules = rules

    def get_name(self) -> str:
        return self.name

    async def check_conditions(self, data: Any = None) -> Optional[Dict[str, Any]]:
        """
        Evalúa las reglas dinámicas usando analysis_tools.
        """
        try:
            from .analysis_tools import run_dynamic_analysis
            
            # Reutilizamos la lógica de analysis_tools
            analysis_result = await run_dynamic_analysis(self.symbol, self.timeframe, self.rules)
            
            if analysis_result.get("status") != "success":
                return None

            events = analysis_result["data"]["events"]
            if not events:
                return None

            # Tomar el último evento
            last_event = events[-1]
            
            # Determinar acción basada en reglas
            action = self.rules.get("action", "alert")
            
            if action in ["buy", "sell"]:
                self.last_evaluation = datetime.now().isoformat()
                return {
                    "action": action,
                    "volume": self.rules.get("volume", 0.01),
                    "sl_pips": self.rules.get("sl_pips"),
                    "tp_pips": self.rules.get("tp_pips"),
                    "comment": f"Strategy {self.name}"
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error evaluando DynamicStrategy {self.name}: {e}")
            return None

# ============================================================================
# MOTOR DE ESTRATEGIAS
# ============================================================================

class StrategyEngine:
    """Motor de gestión de estrategias."""
    
    def __init__(self):
        self.strategies: Dict[str, Strategy] = {}
        self.running = False
        self._monitor_task = None
        
    async def initialize(self):
        """Inicializa el motor de estrategias."""
        logger.info("Inicializando Strategy Engine (OOP)...")
        self.running = True
        self._monitor_task = asyncio.create_task(self.run_tick_evaluation())
        return True
        
    async def shutdown(self):
        """Detiene el motor."""
        self.running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Strategy Engine detenido")

    def register_strategy(self, strategy: Strategy):
        """Registra una instancia de estrategia."""
        self.strategies[strategy.id] = strategy
        logger.info(f"Estrategia registrada: {strategy.name} ({strategy.id})")

    async def create_strategy(self, name: str, symbol: str, timeframe: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Crea y registra una DynamicStrategy."""
        strategy = DynamicStrategy(name, symbol, timeframe, rules)
        self.register_strategy(strategy)
        return {"status": "success", "strategy_id": strategy.id, "strategy": strategy.get_info()}

    async def activate_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """Activa una estrategia."""
        if strategy_id not in self.strategies:
            return {"error": "Estrategia no encontrada", "status": "error"}
        
        self.strategies[strategy_id].status = "running"
        logger.info(f"Estrategia {strategy_id} iniciada")
        return {"status": "success", "message": f"Estrategia {strategy_id} iniciada"}

    async def deactivate_strategy(self, strategy_id: str) -> Dict[str, Any]:
        """Detiene una estrategia."""
        if strategy_id not in self.strategies:
            return {"error": "Estrategia no encontrada", "status": "error"}
        
        self.strategies[strategy_id].status = "stopped"
        logger.info(f"Estrategia {strategy_id} detenida")
        return {"status": "success", "message": f"Estrategia {strategy_id} detenida"}

    async def get_strategy_status(self, strategy_id: str) -> Dict[str, Any]:
        """Obtiene el estado de una estrategia."""
        if strategy_id not in self.strategies:
            return {"error": "Estrategia no encontrada", "status": "error"}
        return {"status": "success", "data": self.strategies[strategy_id].get_info()}

    async def run_tick_evaluation(self):
        """
        Bucle principal de monitoreo (tick evaluation).
        Itera sobre estrategias activas y evalúa condiciones.
        """
        logger.info("Iniciando bucle de evaluación de estrategias (run_tick_evaluation)")
        while self.running:
            try:
                for s_id, strategy in self.strategies.items():
                    if strategy.status == "running":
                        await self._evaluate_strategy(strategy)
                
                await asyncio.sleep(60)  # Intervalo de evaluación
            except Exception as e:
                logger.error(f"Error en run_tick_evaluation: {e}")
                await asyncio.sleep(60)

    async def _evaluate_strategy(self, strategy: Strategy):
        """Evalúa una estrategia específica y ejecuta señales."""
        try:
            signal = await strategy.check_conditions()
            
            if signal:
                action = signal.get("action")
                if action in ["buy", "sell"]:
                    logger.info(f"SEÑAL {action.upper()} generada por estrategia {strategy.id}")
                    
                    # Construir parámetros para TradingEngine
                    trade_params = {
                        "symbol": strategy.symbol,
                        "order_type": f"market_{action}",
                        "volume": signal.get("volume"),
                        "stop_loss_pips": signal.get("sl_pips"),
                        "take_profit_pips": signal.get("tp_pips"),
                        "comment": signal.get("comment")
                    }
                    
                    # Ejecutar trade via TradingEngine
                    from .trading_engine import trading_engine
                    result = await trading_engine.handle_direct_tool_call("open_trade", trade_params)
                    logger.info(f"Resultado ejecución estrategia: {result}")
                    
                    # Registrar trade en la estrategia
                    strategy.trades.append({
                        "timestamp": datetime.now().isoformat(),
                        "signal": signal,
                        "result": result
                    })
                    
        except Exception as e:
            logger.error(f"Error evaluando estrategia {strategy.id}: {e}")

    async def backtest_strategy(self, symbol: str, timeframe: str, rules: Dict[str, Any], days: int = 30) -> Dict[str, Any]:
        """
        Ejecuta un backtest rápido (delegado a backtester.py para versión completa).
        """
        try:
            from .analysis_tools import run_dynamic_analysis
            
            # Versión rápida basada en analysis_tools
            analysis_result = await run_dynamic_analysis(symbol, timeframe, {**rules, "days": days})
            
            if analysis_result.get("status") != "success":
                return analysis_result
                
            events = analysis_result["data"]["events"]
            
            return {
                "status": "success",
                "data": {
                    "symbol": symbol,
                    "days_tested": days,
                    "total_signals": len(events),
                    "signals": events,
                    "performance_metrics": {
                        "profit_factor": 0.0,  # Placeholder
                        "drawdown": 0.0  # Placeholder
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error en backtest: {e}")
            return {"error": str(e), "status": "error"}

# Instancia global
strategy_engine = StrategyEngine()
