from app.core.database import get_connection


def obtener_estadisticas():
    """Obtiene las estadísticas generales desde la vista de la base de datos."""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM vista_estadisticas")
            result = cursor.fetchone()
            
            # Si no hay resultado, devolver valores por defecto
            if not result:
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
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        from datetime import datetime
        return {
            "total_traducciones": 0,
            "total_contribuciones": 0,
            "contribuciones_pendientes": 0,
            "contribuciones_aprobadas": 0,
            "senas_oficiales": 0,
            "reportes_activos": 0,
            "precision_modelo": 0.0,
            "fecha_actualizacion": datetime.now()
        }
    finally:
        if 'conn' in locals() and conn:
            conn.close()
