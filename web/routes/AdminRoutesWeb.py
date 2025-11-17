from flask import Blueprint, render_template, request, jsonify
from web.middleware.auth_web import login_required, role_required
from web.controller.EstadisticasControllerWeb import EstadisticasControllerWeb
from web.config.db import get_db_connection

web_admin = Blueprint("web_admin", __name__)


@web_admin.route("/admin/dashboard", methods=["GET"])
@login_required
@role_required([1, 3])
def dashboard():
    resp = EstadisticasControllerWeb.obtener_estadisticas()
    stats = resp.get("data") if resp.get("status") == 200 else None
    return render_template("admin/dashboard.html", stats=stats)

@web_admin.route("/contribuciones", methods=["GET"])
@login_required
def contribuciones():
    # Fetch contributions from DB
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Only load pending contributions for admin review
            cur.execute("SELECT id_contribucion, palabra_asociada, descripcion, archivo_video, estado, fecha_contribucion FROM contribuciones_senas WHERE estado = 'pendiente' ORDER BY fecha_contribucion DESC")
            contribs = cur.fetchall()
    finally:
        conn.close()
    pending_count = len(contribs) if contribs else 0
    return render_template("admin/contribuciones.html", contribuciones=contribs, pending_count=pending_count)


@web_admin.route('/admin/contribuciones/approve/<int:id_contribucion>', methods=['POST'])
@login_required
@role_required([1,3])
def approve_contribucion(id_contribucion):
    # Mark contribution as approved
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE contribuciones_senas SET estado='aprobada', fecha_gestion=NOW() WHERE id_contribucion=%s", (id_contribucion,))
            conn.commit()
    finally:
        conn.close()
    return jsonify({'status': 'ok', 'id': id_contribucion})


@web_admin.route('/admin/contribuciones/delete/<int:id_contribucion>', methods=['POST'])
@login_required
@role_required([1,3])
def delete_contribucion(id_contribucion):
    # Delete a contribution (admin)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM contribuciones_senas WHERE id_contribucion=%s", (id_contribucion,))
            conn.commit()
    finally:
        conn.close()
    return jsonify({'status': 'ok', 'id': id_contribucion})


@web_admin.route('/admin/reportes', methods=['GET'])
@login_required
@role_required([1,3])
def reportes():
    # Fetch reports, allow filtering by estado via query param
    estado_filter = request.args.get('estado', None)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if estado_filter == 'pendiente':
                cur.execute("SELECT id_reporte, id_traduccion, tipo_traduccion, descripcion_error, evidencia_url, prioridad, estado, fecha_reporte, id_usuario_reporta FROM reportes_errores WHERE estado = 'pendiente' ORDER BY fecha_reporte DESC")
            elif estado_filter == 'en_revision':
                cur.execute("SELECT id_reporte, id_traduccion, tipo_traduccion, descripcion_error, evidencia_url, prioridad, estado, fecha_reporte, id_usuario_reporta FROM reportes_errores WHERE estado = 'en_revision' ORDER BY fecha_reporte DESC")
            else:
                # default: show both pendiente and en_revision
                cur.execute("SELECT id_reporte, id_traduccion, tipo_traduccion, descripcion_error, evidencia_url, prioridad, estado, fecha_reporte, id_usuario_reporta FROM reportes_errores WHERE estado IN ('pendiente','en_revision') ORDER BY fecha_reporte DESC")
            reports = cur.fetchall()
    finally:
        conn.close()
    pending_count = len(reports) if reports else 0
    return render_template('admin/reportes.html', reportes=reports, pending_count=pending_count, current_filter=estado_filter)


@web_admin.route('/admin/reportes/review/<int:id_reporte>', methods=['POST'])
@login_required
@role_required([1,3])
def review_reporte(id_reporte):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE reportes_errores SET estado='en_revision' WHERE id_reporte=%s", (id_reporte,))
            conn.commit()
    finally:
        conn.close()
    return jsonify({'status': 'ok', 'id': id_reporte})


@web_admin.route('/admin/reportes/delete/<int:id_reporte>', methods=['POST'])
@login_required
@role_required([1,3])
def delete_reporte(id_reporte):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM reportes_errores WHERE id_reporte=%s", (id_reporte,))
            conn.commit()
    finally:
        conn.close()
    return jsonify({'status': 'ok', 'id': id_reporte})