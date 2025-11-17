from flask import Blueprint, render_template, request, flash, redirect, url_for
from web.controller.vista_controller_web import VistaControllerWeb
from web.middleware.auth_web import login_required, role_required
from web.controller.admin_controller_web import AdminControllerWeb
from web.controller.usuario_controller_web import UsuarioControllerWeb
from flask import session


web_admin = Blueprint("web_admin", __name__)


# Dashboard Admin — muestra estadísticas agregadas
@web_admin.route("/admin/dashboard", methods=["GET"])
@login_required
@role_required([1, 3])
def admin_dashboard():
    stats = VistaControllerWeb.obtener_estadisticas()
    return render_template("admin/dashboard.html", stats=stats)

# Contribuciones Admin
@web_admin.route("/contribuciones", methods=["GET"])
@login_required
@role_required([1, 3])
def contribuciones():
    contribs = AdminControllerWeb.obtener_contribuciones_pendientes()
    pending_count = len(contribs) if contribs else 0
    return render_template("admin/contribuciones.html", contribuciones=contribs, pending_count=pending_count)

# Approve or Delete Contribuciones
@web_admin.route('/admin/contribuciones/approve/<int:id_contribucion>', methods=['POST'])
@login_required
@role_required([1,3])
def approve_contribucion(id_contribucion):
    AdminControllerWeb.aprobar_contribucion(id_contribucion)
    flash('Contribución aprobada.', 'success')
    return redirect(url_for('web_admin.contribuciones'))

# Delete Contribuciones
@web_admin.route('/admin/contribuciones/delete/<int:id_contribucion>', methods=['POST'])
@login_required
@role_required([1,3])
def delete_contribucion(id_contribucion):
    AdminControllerWeb.eliminar_contribucion(id_contribucion)
    flash('Contribución eliminada.', 'success')
    return redirect(url_for('web_admin.contribuciones'))

# Reportes Admin
@web_admin.route('/admin/reportes', methods=['GET'])
@login_required
@role_required([1,3])
def reportes():
    estado_filter = request.args.get('estado', None)
    reports = AdminControllerWeb.obtener_reportes(estado_filter)
    pending_count = len(reports) if reports else 0
    return render_template('admin/reportes.html', reportes=reports, pending_count=pending_count, current_filter=estado_filter)

# Mark Reporte as In Review
@web_admin.route('/admin/reportes/review/<int:id_reporte>', methods=['POST'])
@login_required
@role_required([1,3])
def review_reporte(id_reporte):
    AdminControllerWeb.poner_reporte_en_revision(id_reporte)
    flash('Reporte puesto en revisión.', 'success')
    return redirect(url_for('web_admin.reportes'))

# Delete Reporte
@web_admin.route('/admin/reportes/delete/<int:id_reporte>', methods=['POST'])
@login_required
@role_required([1,3])
def delete_reporte(id_reporte):
    AdminControllerWeb.eliminar_reporte(id_reporte)
    flash('Reporte eliminado.', 'success')
    return redirect(url_for('web_admin.reportes'))

# Users Management Page
@web_admin.route('/admin/usuarios', methods=['GET'])
@login_required
@role_required([1,3])
def admin_usuarios():
    # Delegar al controlador la obtención de usuarios (separación de responsabilidades)
    search = request.args.get('search', None)
    usuarios = UsuarioControllerWeb.listar_usuarios(limit=100, search=search)
    return render_template('admin/usuarios.html', usuarios=usuarios, search=search)


# Delete User (solo rol 3 puede eliminar)
@web_admin.route('/admin/usuarios/delete/<int:id_usuario>', methods=['POST'])
@login_required
@role_required([1,3])
def delete_usuario(id_usuario):
    actor_id = session.get('user_id')
    actor_role = session.get('rol')

    # No permitir eliminarse a sí mismo
    if actor_id == id_usuario:
        flash('No puedes eliminar tu propia cuenta.', 'error')
        return redirect(url_for('web_admin.admin_usuarios'))

    # Obtener información del usuario objetivo
    from web.models.usuario_model import UsuarioModel
    objetivo = UsuarioModel.obtener_por_id(id_usuario)
    if not objetivo:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('web_admin.admin_usuarios'))

    target_role = objetivo.get('id_rol') if isinstance(objetivo, dict) else objetivo['id_rol']

    # Si el actor es rol 1 (administrador), sólo puede eliminar rol 2 (colaborador)
    if actor_role == 1 and target_role != 2:
        flash('Los administradores solo pueden eliminar colaboradores (rol 2).', 'error')
        return redirect(url_for('web_admin.admin_usuarios'))

    # Rol 3 puede eliminar cualquiera (salvo sí mismo ya bloqueado arriba)
    res = UsuarioControllerWeb.eliminar_usuario(id_usuario)
    if res.get('status') == 200:
        flash('Usuario eliminado correctamente.', 'success')
        return redirect(url_for('web_admin.admin_usuarios'))
    # Passthrough error
    flash(res.get('error', 'Error al eliminar usuario.'), 'error')
    return redirect(url_for('web_admin.admin_usuarios'))
