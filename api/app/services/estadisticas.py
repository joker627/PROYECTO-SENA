"""Servicios de estadísticas del sistema.

Capa de lógica de negocio para obtención de estadísticas agregadas,
con manejo robusto de excepciones."""

import pymysql
from datetime import datetime
from fastapi import HTTPException, status
from app.core.database import get_connection
from app.core.logger import logger


def obtener_estadisticas():
    """Obtiene las estadísticas generales desde la vista de la base de datos."""
    conn = None
    try:
        conn = get_connection()
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM vista_estadisticas")
            result = cursor.fetchone()
            
            # Si no hay resultado, devolver valores por defecto
            if not result:
                logger.warning("No se encontraron estadísticas en vista_estadisticas")
                return {
                    "total_traducciones": 0,
                    "total_contribuciones": 0,
                    "contribuciones_pendientes": 0,
                    "contribuciones_aprobadas": 0,
                    "senas_oficiales": 0,
                    "reportes_activos": 0,
                    "precision_modelo": 0.0,
                    "fecha_actualizacion": None
                }
            
            # Asegurar que no haya valores NULL
            return {
                "total_traducciones": result.get("total_traducciones") or 0,
                "total_contribuciones": result.get("total_contribuciones") or 0,
                "contribuciones_pendientes": result.get("contribuciones_pendientes") or 0,
                "contribuciones_aprobadas": result.get("contribuciones_aprobadas") or 0,
                "senas_oficiales": result.get("senas_oficiales") or 0,
                "reportes_activos": result.get("reportes_activos") or 0,
                "precision_modelo": float(result.get("precision_modelo") or 0.0),
                "fecha_actualizacion": result.get("fecha_actualizacion")
            }
            
    except pymysql.MySQLError as e:
        logger.error(f"Error de BD en obtener_estadisticas: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener estadísticas"
        )
    except Exception as e:
        logger.error(f"Error inesperado en obtener_estadisticas: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error cerrando conexión: {e}")
