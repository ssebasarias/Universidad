"""Paquete de utilidades de ingestión.

Exponer funciones comunes desde submódulos si es necesario.
"""

from .db import get_conn, create_table, save_message, get_conversation

__all__ = ["get_conn", "create_table", "save_message", "get_conversation"]
