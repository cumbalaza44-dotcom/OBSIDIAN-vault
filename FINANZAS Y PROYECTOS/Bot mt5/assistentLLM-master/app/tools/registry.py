"""
Tool registry para registrar y recuperar herramientas disponibles para el LLM.
Cada módulo de herramienta debe usar el decorador @register_tool("name", meta={...})
y exportar una función `run(args: dict) -> dict` (puede ser async o sync).
"""
from typing import Callable, Dict, Any, Optional
from pydantic import BaseModel

_TOOLS: Dict[str, Dict[str, Any]] = {}


def register_tool(name: str, meta: Dict[str, Any]):
    """Decorator to register a tool.

    Usage:
        @register_tool('get_account_info', TOOL_META)
        async def run(args):
            ...
    """
    def decorator(func: Callable):
        # meta can optionally contain a 'schema' key which is a Pydantic model class
        schema: Optional[type] = meta.get('schema') if isinstance(meta, dict) else None
        if schema is not None and not issubclass(schema, BaseModel):
            raise TypeError("meta['schema'] must be a Pydantic BaseModel subclass if provided")

        _TOOLS[name] = {
            "meta": meta,
            "schema": schema,
            "run": func
        }
        return func
    return decorator


def get_tool(name: str):
    """Returns the tool dict or None if not found."""
    return _TOOLS.get(name)


def list_tools():
    return list(_TOOLS.keys())


# Auto-discover tools in the app.tools package so that modules using @register_tool are loaded
def _load_all_tools():
    try:
        import pkgutil
        import importlib
        import app.tools as tools_pkg

        for finder, name, ispkg in pkgutil.iter_modules(tools_pkg.__path__):
            # skip the registry module to avoid re-import loops
            if name == 'registry':
                continue
            full_name = f"{tools_pkg.__name__}.{name}"
            try:
                importlib.import_module(full_name)
            except Exception as e:
                # Print exception to help test diagnostics (tests run in CI/locally)
                print(f"[registry] failed to import tool module {full_name}: {e}")
                # Also raise during local dev if DEBUG env set
                import os
                if os.environ.get('TOOLS_DEBUG'):
                    raise
                continue
    except Exception:
        pass


# Ejecutar la carga automática al importar este módulo
_load_all_tools()

# Example: if in the future a tool places orders, register with meta like:
# TOOL_META = {"name": "place_order", "description": "Place a market order", "requires_confirmation": True, "risk_level": "high", "schema": PlaceOrderSchema}
