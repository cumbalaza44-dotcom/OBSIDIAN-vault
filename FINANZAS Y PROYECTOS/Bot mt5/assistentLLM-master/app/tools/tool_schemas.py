from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field


class GetHistoricalDataSchema(BaseModel):
    symbol: str = Field(..., description="Nombre del símbolo, e.g. 'EURUSD'")
    timeframe: str = Field(..., description="Timeframe, e.g. 'M1','H1'")
    count: Optional[int] = Field(100, ge=1, description="Número de barras a solicitar")


class GetSymbolInfoSchema(BaseModel):
    symbol: str = Field(..., description="Nombre del símbolo a consultar")


class RunDynamicAnalysisSchema(BaseModel):
    symbol: str = Field(..., description="Símbolo a analizar")
    timeframe: str = Field(..., description="Timeframe de las velas")
    strategy: str = Field(..., description="Nombre de la estrategia, e.g. 'ema_cross'")
    days: Optional[int] = Field(2, ge=1)
    fast_period: Optional[int] = Field(12, ge=1)
    slow_period: Optional[int] = Field(26, ge=1)
    extra_indicators: Optional[List[Any]] = Field(None, description="Lista opcional de indicadores/descriptores")

    class Config:
        extra = 'allow'  # permitimos campos adicionales para flexibilidad


_SCHEMAS = {
    "get_historical_data": GetHistoricalDataSchema,
    "get_symbol_info": GetSymbolInfoSchema,
    "run_dynamic_analysis": RunDynamicAnalysisSchema
}

# Additional schemas for other tools
from pydantic import conint


class GetSymbolPriceSchema(BaseModel):
    symbol: str


class CompareVolatilitySchema(BaseModel):
    symbol_a: str
    symbol_b: str
    period: conint(ge=1) = 14


class CheckCorrelationSchema(BaseModel):
    symbol_a: str
    symbol_b: str
    period: conint(ge=1) = 30


class CalculateRsiSchema(BaseModel):
    symbol: str
    length: conint(ge=1) = 14
    count: conint(ge=1) = 100


class ListOpenPositionsSchema(BaseModel):
    # no args required
    pass


class GetAccountBalanceSchema(BaseModel):
    # no args required
    pass


_SCHEMAS.update({
    "get_symbol_price": GetSymbolPriceSchema,
    "get_account_balance": GetAccountBalanceSchema,
    "list_open_positions": ListOpenPositionsSchema,
    "compare_volatility": CompareVolatilitySchema,
    "check_correlation": CheckCorrelationSchema,
    "calculate_rsi": CalculateRsiSchema
})


def get_schema(name: str):
    return _SCHEMAS.get(name)
