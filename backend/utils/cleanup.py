# Utilidades para limpieza de datos
from models.user_model import cleanup_expired_anonymous_sessions


def cleanup_old_anonymous_sessions(days_old=30):
    try:
        deleted_count = cleanup_expired_anonymous_sessions(days_old)
        print(f"Se eliminaron {deleted_count} sesiones anónimas expiradas")
        return deleted_count
    except Exception as e:
        print(f"Error en limpieza de sesiones: {e}")
        return 0


if __name__ == "__main__":
    # Ejecutar limpieza si se llama directamente
    cleanup_old_anonymous_sessions()