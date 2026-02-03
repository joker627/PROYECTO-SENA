from app.core.database import get_connection
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password

def obtener_usuarios(skip: int = 0, limit: int = 100, rol: int = None, estado: str = None, query: str = None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Base query
            sql = "SELECT u.*, r.nombre_rol FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol WHERE 1=1"
            count_sql = "SELECT COUNT(*) as total FROM usuarios u WHERE 1=1"
            params = []
            
            if rol:
                sql += " AND u.id_rol = %s"
                count_sql += " AND u.id_rol = %s"
                params.append(rol)
            
            if estado:
                sql += " AND u.estado = %s"
                count_sql += " AND u.estado = %s"
                params.append(estado)
                
            if query:
                # Search by name, email or document
                search_term = f"%{query}%"
                sql += " AND (u.nombre_completo LIKE %s OR u.correo LIKE %s OR u.numero_documento LIKE %s)"
                count_sql += " AND (u.nombre_completo LIKE %s OR u.correo LIKE %s OR u.numero_documento LIKE %s)"
                params.extend([search_term, search_term, search_term])

            # Get Total (with filters)
            cursor.execute(count_sql, tuple(params))
            total = cursor.fetchone()['total']
            
            # Get Data (with filters + pagination)
            sql += " ORDER BY u.fecha_registro DESC LIMIT %s OFFSET %s"
            # Need to create a new tuple for data query that includes limit/offset
            data_params = params.copy()
            data_params.extend([limit, skip])
            
            cursor.execute(sql, tuple(data_params))
            data = cursor.fetchall()
            
            return {"total": total, "data": data}
    finally:
        conn.close()

def obtener_usuario_por_id(id_usuario: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT u.*, r.nombre_rol FROM usuarios u JOIN roles r ON u.id_rol = r.id_rol WHERE u.id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            return cursor.fetchone()
    finally:
        conn.close()

def crear_usuario(usuario: UsuarioCreate):
    conn = get_connection()
    try:
        hashed_password = hash_password(usuario.contrasena)
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO usuarios (nombre_completo, correo, contrasena, tipo_documento, numero_documento, id_rol, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario.nombre_completo, usuario.correo, hashed_password,
                usuario.tipo_documento, usuario.numero_documento, usuario.id_rol, usuario.estado
            ))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()

def actualizar_usuario(id_usuario: int, usuario: UsuarioUpdate):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Construir query dinámica
            fields = []
            values = []
            if usuario.nombre_completo:
                fields.append("nombre_completo=%s")
                values.append(usuario.nombre_completo)
            if usuario.correo:
                fields.append("correo=%s")
                values.append(usuario.correo)
            if usuario.contrasena:
                from app.core.security import hash_password
                fields.append("contrasena=%s")
                values.append(hash_password(usuario.contrasena))
            if usuario.tipo_documento:
                fields.append("tipo_documento=%s")
                values.append(usuario.tipo_documento)
            if usuario.numero_documento:
                fields.append("numero_documento=%s")
                values.append(usuario.numero_documento)
            if usuario.imagen_perfil:
                fields.append("imagen_perfil=%s")
                values.append(usuario.imagen_perfil)
            if usuario.id_rol:
                fields.append("id_rol=%s")
                values.append(usuario.id_rol)
            if usuario.estado:
                fields.append("estado=%s")
                values.append(usuario.estado)
            
            if not fields:
                return False
                
            values.append(id_usuario)
            sql = f"UPDATE usuarios SET {', '.join(fields)} WHERE id_usuario=%s"
            cursor.execute(sql, tuple(values))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()

def eliminar_usuario(id_usuario: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0
    finally:
        conn.close()

def obtener_stats_usuarios():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN id_rol = 1 THEN 1 ELSE 0 END) as administradores,
                SUM(CASE WHEN id_rol = 2 THEN 1 ELSE 0 END) as colaboradores,
                SUM(CASE WHEN estado = 'activo' THEN 1 ELSE 0 END) as activos
            FROM usuarios
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            # Ensure no None values
            return {
                "total": result.get('total', 0) or 0,
                "administradores": int(result.get('administradores', 0) or 0),
                "colaboradores": int(result.get('colaboradores', 0) or 0),
                "activos": int(result.get('activos', 0) or 0)
            }
    finally:
        conn.close()
