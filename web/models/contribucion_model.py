from web.config.db import get_db_connection


class ContribucionModel:
    @staticmethod
    def listar_pendientes():
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id_contribucion, palabra_asociada, descripcion, archivo_video, estado, fecha_contribucion FROM contribuciones_senas WHERE estado = 'pendiente' ORDER BY fecha_contribucion DESC")
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def aprobar(id_contribucion):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE contribuciones_senas SET estado='aprobada', fecha_gestion=NOW() WHERE id_contribucion=%s", (id_contribucion,))
                conn.commit()
                return cur.rowcount
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_contribucion):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM contribuciones_senas WHERE id_contribucion=%s", (id_contribucion,))
                conn.commit()
                return cur.rowcount
        finally:
            conn.close()
