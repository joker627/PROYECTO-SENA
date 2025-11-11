from flask import Blueprint, request, redirect, url_for, flash
from backend.models.usuarios_models import (
    create_user,
    update_user_role,
    update_user_estado,
    delete_user_by_id,
    delete_user_by_email,
)


usuarios_bp = Blueprint('usuarios_bp', __name__)


@usuarios_bp.route('/admin/usuarios/crear', methods=['POST'])
def crear_usuario():
    """Create a new usuario from the admin UI form."""
    nombre = request.form.get('nombre_completo') or request.form.get('nombre')
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena') or request.form.get('password')
    id_rol = request.form.get('id_rol') or request.form.get('rol') or 2
    try:
        id_rol = int(id_rol)
    except Exception:
        id_rol = 2

    new_id = create_user(nombre or '', correo or '', contrasena or '', id_rol)
    if new_id:
        flash('Usuario creado correctamente.', 'success')
    else:
        flash('No se pudo crear el usuario.', 'danger')
    return redirect(url_for('general_bp.admin_usuarios'))


@usuarios_bp.route('/admin/usuarios/<int:id_usuario>/cambiar_rol', methods=['POST'])
def cambiar_rol(id_usuario):
    id_rol = request.form.get('id_rol') or request.form.get('rol')
    try:
        id_rol = int(id_rol)
    except Exception:
        flash('Rol inválido.', 'warning')
        return redirect(url_for('general_bp.admin_usuarios'))

    ok = update_user_role(id_usuario, id_rol)
    if ok:
        flash('Rol actualizado.', 'success')
    else:
        flash('No se pudo actualizar el rol.', 'danger')
    return redirect(url_for('general_bp.admin_usuarios'))


@usuarios_bp.route('/admin/usuarios/<int:id_usuario>/cambiar_estado', methods=['POST'])
def cambiar_estado(id_usuario):
    estado = request.form.get('estado') or request.form.get('estado_usuario') or 'inactivo'
    ok = update_user_estado(id_usuario, estado)
    if ok:
        flash('Estado actualizado.', 'success')
    else:
        flash('No se pudo actualizar el estado.', 'danger')
    return redirect(url_for('general_bp.admin_usuarios'))


@usuarios_bp.route('/admin/usuarios/<int:id_usuario>/eliminar', methods=['POST'])
def eliminar_usuario(id_usuario):
    ok = delete_user_by_id(id_usuario)
    if ok:
        flash('Usuario eliminado.', 'success')
    else:
        flash('No se pudo eliminar el usuario.', 'danger')
    return redirect(url_for('general_bp.admin_usuarios'))


@usuarios_bp.route('/admin/usuarios/eliminar_por_email', methods=['POST'])
def eliminar_por_email():
    # Accept 'correo' (template) or legacy 'email_usuario' field
    correo = request.form.get('correo') or request.form.get('email_usuario')
    motivo = request.form.get('motivo_eliminacion') or request.form.get('motivo')

    if not correo:
        flash('Correo requerido.', 'warning')
        return redirect(url_for('general_bp.admin_usuarios'))

    affected = delete_user_by_email(correo)
    if affected is None:
        flash('Error al eliminar por correo.', 'danger')
    elif affected == 0:
        flash('No se encontró ningún usuario con ese correo.', 'info')
    else:
        msg = f'Se eliminaron {affected} usuario(s).'
        if motivo:
            msg = msg + f' Motivo: {motivo}'
        flash(msg, 'success')
    return redirect(url_for('general_bp.admin_usuarios'))
