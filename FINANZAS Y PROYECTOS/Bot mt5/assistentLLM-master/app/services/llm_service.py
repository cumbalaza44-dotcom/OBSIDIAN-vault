"""
LLMService - Abstrae toda la comunicación con la API de Google Gemini.
Responsabilidades:
- Construir prompts y definir herramientas en formato requerido por la API
- Gestionar la clave de API de Google
- Procesar respuestas del LLM
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
import json

# Importación condicional de Google Generative AI
try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    logging.warning("Google Generative AI no está disponible. El servicio funcionará en modo simulación.")

from ..core.config import get_settings

logger = logging.getLogger(__name__)

class LLMService:
    """Servicio para comunicación con Google Gemini."""
    
    def __init__(self):
        self.model = None
        self.tools = []
        self.conversation_history = []
        self.initialized = False
        
        # Configuración
        self.settings = get_settings()
        
    def initialize(self) -> bool:
        """
        Inicializa el servicio de LLM.
        
        Returns:
            bool: True si la inicialización fue exitosa
        """
        if not GOOGLE_AI_AVAILABLE:
            logger.error("Google Generative AI no está disponible")
            return False
        
        try:
            # Configurar la API key
            api_key = self.settings.google_api_key
            if not api_key:
                logger.error("API key de Google no configurada")
                return False
            
            genai.configure(api_key=api_key)
            
            # Inicializar el modelo
            self.model = genai.GenerativeModel('gemini-pro')
            
            self.initialized = True
            logger.info("LLM Service inicializado correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error inicializando LLM Service: {e}")
            return False
    
    def add_tool(self, tool_definition: Dict[str, Any]):
        """
        Agrega una herramienta al contexto del LLM.
        
        Args:
            tool_definition: Definición de la herramienta en formato Google AI
        """
        self.tools.append(tool_definition)
        logger.info(f"Herramienta agregada: {tool_definition.get('name', 'Unknown')}")
    
    def clear_tools(self):
        """Limpia todas las herramientas del contexto."""
        self.tools.clear()
        logger.info("Herramientas limpiadas")
    
    def add_to_conversation(self, role: str, content: str):
        """
        Agrega un mensaje al historial de conversación.
        
        Args:
            role: Rol del mensaje ('user' o 'assistant')
            content: Contenido del mensaje
        """
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": self._get_timestamp()
        })
    
    def clear_conversation(self):
        """Limpia el historial de conversación."""
        self.conversation_history.clear()
        logger.info("Historial de conversación limpiado")
    
    async def process_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        use_tools: bool = True
    ) -> Dict[str, Any]:
        """
        Procesa un prompt a través del LLM.
        
        Args:
            prompt: El prompt del usuario
            context: Contexto adicional (opcional)
            use_tools: Si debe usar las herramientas disponibles
            
        Returns:
            Dict con la respuesta del LLM
        """
        if not self.initialized:
            return {
                "error": "LLM Service no inicializado",
                "status": "error"
            }
        
        try:
            # Construir el prompt completo
            full_prompt = self._build_prompt(prompt, context)
            
            # Agregar a la conversación
            self.add_to_conversation("user", prompt)
            
            # Configurar el modelo con herramientas si es necesario
            if use_tools and self.tools:
                model_with_tools = genai.GenerativeModel(
                    'gemini-pro',
                    tools=self.tools
                )
            else:
                model_with_tools = self.model
            
            # Generar respuesta
            response = await self._generate_response(model_with_tools, full_prompt)
            
            # Procesar la respuesta
            processed_response = self._process_response(response)
            
            # Agregar respuesta a la conversación
            self.add_to_conversation("assistant", processed_response.get("content", ""))
            
            return processed_response
            
        except Exception as e:
            logger.error(f"Error procesando prompt: {e}")
            return {
                "error": f"Error procesando prompt: {str(e)}",
                "status": "error"
            }
    
    def _build_prompt(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Construye el prompt completo con contexto.
        
        Args:
            prompt: Prompt del usuario
            context: Contexto adicional
            
        Returns:
            Prompt completo
        """
        system_prompt = """Eres un asistente de trading especializado en análisis de mercados financieros y ejecución de operaciones a través de MetaTrader 5. 

Tus responsabilidades incluyen:
- Analizar datos de mercado y proporcionar insights
- Ejecutar órdenes de trading cuando se solicite
- Gestionar posiciones abiertas
- Proporcionar análisis técnico y fundamental
- Responder preguntas sobre el estado de la cuenta y operaciones

Siempre proporciona respuestas claras, precisas y útiles. Si no estás seguro de algo, indícalo claramente."""
        
        full_prompt = system_prompt + "\n\n"
        
        # Agregar contexto si existe
        if context:
            full_prompt += f"Contexto adicional: {json.dumps(context, indent=2)}\n\n"
        
        # Agregar historial de conversación reciente (últimos 5 mensajes)
        recent_history = self.conversation_history[-10:] if self.conversation_history else []
        if recent_history:
            full_prompt += "Historial reciente de la conversación:\n"
            for msg in recent_history:
                full_prompt += f"{msg['role'].title()}: {msg['content']}\n"
            full_prompt += "\n"
        
        full_prompt += f"Usuario: {prompt}\n\nAsistente:"
        
        return full_prompt
    
    async def _generate_response(self, model, prompt: str):
        """
        Genera una respuesta usando el modelo.
        
        Args:
            model: Modelo de Google AI
            prompt: Prompt completo
            
        Returns:
            Respuesta del modelo
        """
        try:
            response = model.generate_content(prompt)
            # model.generate_content may be async (returns a coroutine) or sync; handle both
            if asyncio.iscoroutine(response):
                response = await response
            return response
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            raise
    
    def _process_response(self, response) -> Dict[str, Any]:
        """
        Procesa la respuesta del LLM.
        
        Args:
            response: Respuesta del modelo
            
        Returns:
            Respuesta procesada
        """
        try:
            # Extraer el contenido de la respuesta
            content = response.text if hasattr(response, 'text') else str(response)
            
            # Verificar si hay llamadas a herramientas
            tool_calls = []
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call'):
                                tool_calls.append({
                                    "name": part.function_call.name,
                                    "args": part.function_call.args
                                })
            
            return {
                "content": content,
                "tool_calls": tool_calls,
                "status": "success",
                "timestamp": self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"Error procesando respuesta: {e}")
            return {
                "content": "Error procesando la respuesta del LLM",
                "status": "error",
                "error": str(e)
            }
    
    def _get_timestamp(self) -> str:
        """Obtiene el timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen de la conversación actual.
        
        Returns:
            Dict con resumen de la conversación
        """
        return {
            "total_messages": len(self.conversation_history),
            "tools_available": len(self.tools),
            "last_message": self.conversation_history[-1] if self.conversation_history else None
        }

# Instancia global del servicio LLM
llm_service = LLMService() 