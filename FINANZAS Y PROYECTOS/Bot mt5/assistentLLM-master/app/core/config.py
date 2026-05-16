"""
Config - Gestión de configuración del sistema.
Responsabilidades:
- Cargar variables de entorno y configuración
- Proporcionar acceso centralizado a la configuración
- Validar configuración requerida
"""

import os
from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración del sistema."""
    
    # Configuración de la API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_debug: bool = Field(default=False, env="API_DEBUG")
    
    # Configuración de Google AI
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    google_model: str = Field(default="gemini-pro", env="GOOGLE_MODEL")
    
    # Configuración de MT5
    mt5_login: Optional[int] = Field(default=None, env="MT5_LOGIN")
    mt5_password: Optional[str] = Field(default=None, env="MT5_PASSWORD")
    mt5_server: Optional[str] = Field(default=None, env="MT5_SERVER")
    
    # Configuración de logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # Configuración de seguridad
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    api_key_header: str = Field(default="X-API-Key", env="API_KEY_HEADER")
    
    # Configuración de estado
    state_backend: str = Field(default="memory", env="STATE_BACKEND")  # memory, redis
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    
    # Configuración de herramientas
    max_tool_execution_time: int = Field(default=30, env="MAX_TOOL_EXECUTION_TIME")
    max_conversation_history: int = Field(default=100, env="MAX_CONVERSATION_HISTORY")
    # Retry policy
    max_tool_retries: int = Field(default=2, env="MAX_TOOL_RETRIES")
    retry_backoff_base: float = Field(default=0.5, env="RETRY_BACKOFF_BASE")
    # Compensator worker
    enable_compensator_worker: bool = Field(default=False, env="ENABLE_COMPENSATOR_WORKER")
    # Seguridad de ejecución de órdenes
    enable_order_execution: bool = Field(default=False, env="ENABLE_ORDER_EXECUTION")
    require_double_confirmation: bool = Field(default=True, env="REQUIRE_DOUBLE_CONFIRMATION")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Instancia global de configuración
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """
    Obtiene la instancia de configuración.
    
    Returns:
        Instancia de Settings
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

def validate_configuration() -> bool:
    """
    Valida que la configuración sea correcta.
    
    Returns:
        True si la configuración es válida
    """
    settings = get_settings()
    
    # Validar configuración requerida
    if not settings.google_api_key:
        print("ERROR: GOOGLE_API_KEY no está configurada")
        return False
    
    # Validar configuración opcional pero recomendada
    if not settings.mt5_login or not settings.mt5_password:
        print("ADVERTENCIA: Credenciales de MT5 no configuradas")
        print("El sistema funcionará en modo simulación para MT5")
    
    return True

def print_configuration():
    """Imprime la configuración actual (sin datos sensibles)."""
    settings = get_settings()
    
    print("=== Configuración del Sistema ===")
    print(f"API Host: {settings.api_host}")
    print(f"API Port: {settings.api_port}")
    print(f"API Debug: {settings.api_debug}")
    print(f"Google Model: {settings.google_model}")
    print(f"Log Level: {settings.log_level}")
    print(f"State Backend: {settings.state_backend}")
    print(f"Max Tool Execution Time: {settings.max_tool_execution_time}s")
    print(f"Max Conversation History: {settings.max_conversation_history}")
    
    # Mostrar estado de configuración sensible
    print(f"Google API Key: {'Configurada' if settings.google_api_key else 'NO CONFIGURADA'}")
    print(f"MT5 Credentials: {'Configuradas' if settings.mt5_login and settings.mt5_password else 'NO CONFIGURADAS'}")
    print("=================================") 