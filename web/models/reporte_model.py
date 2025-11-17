from web.config.db import get_db_connection


class ReporteModel:
    @staticmethod
    def listar(estado=None):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                if estado == 'pendiente':
                    cur.execute("SELECT id_reporte, id_traduccion, tipo_traduccion, descripcion_error, evidencia_url, prioridad, estado, fecha_reporte, id_usuario_reporta FROM reportes_errores WHERE estado = 'pendiente' ORDER BY fecha_reporte DESC")
                elif estado == 'en_revision':
                    cur.execute("SELECT id_reporte, id_traduccion, tipo_traduccion, descripcion_error, evidencia_url, prioridad, estado, fecha_reporte, id_usuario_reporta FROM reportes_errores WHERE estado = 'en_revision' ORDER BY fecha_reporte DESC")
                else:
                    cur.execute("SELECT id_reporte, id_traduccion, tipo_traduccion, descripcion_error, evidencia_url, prioridad, estado, fecha_reporte, id_usuario_reporta FROM reportes_errores WHERE estado IN ('pendiente','en_revision') ORDER BY fecha_reporte DESC")
                return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def marcar_en_revision(id_reporte):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE reportes_errores SET estado='en_revision' WHERE id_reporte=%s", (id_reporte,))
                conn.commit()
                return cur.rowcount
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_reporte):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM reportes_errores WHERE id_reporte=%s", (id_reporte,))
                conn.commit()
                return cur.rowcount
        finally:
            conn.close()
