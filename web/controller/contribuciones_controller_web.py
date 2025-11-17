"""
Wrapper de compatibilidad: reexporta `AdminControllerWeb` desde el nuevo
`admin_controller_web.py`. Mantener este archivo temporalmente para evitar
romper imports externos mientras se actualiza el resto del proyecto.
"""

from web.controller.admin_controller_web import AdminControllerWeb  # re-export
