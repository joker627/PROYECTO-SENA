# models/anonimo_model.py
from web.config.db import get_db_connection
from shared.utils.uuid_utils import generar_uuid_anonimo
import datetime

class UsuarioAnonimoModel:

    @staticmethod
    def crear_anonimo():
    
        #Crea un usuario anónimo en la DB y devuelve su UUID.

        conn = get_db_connection()
        uuid_anonimo = generar_uuid_anonimo()

        query = "INSERT INTO usuarios_anonimos (uuid_visitante) VALUES (%s)"
        with conn.cursor() as cursor:
            cursor.execute(query, (uuid_anonimo,))
            conn.commit()
            id_anonimo = cursor.lastrowid

        conn.close()
        return {"id_anonimo": id_anonimo, "uuid": uuid_anonimo}

    @staticmethod
    def obtener_por_uuid(uuid_visitante):

        #Devuelve el registro del usuario anónimo según su UUID.

        conn = get_db_connection()
        query = "SELECT * FROM usuarios_anonimos WHERE uuid_visitante = %s"
        with conn.cursor() as cursor:
            cursor.execute(query, (uuid_visitante,))
            result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def crear_con_uuid(uuid_visitante):
        """
        Inserta un usuario anónimo usando el UUID provisto por el cliente.
        Devuelve el id generado y el uuid insertado.
        """
        conn = get_db_connection()
        query = "INSERT INTO usuarios_anonimos (uuid_visitante, fecha_registro) VALUES (%s, %s)"
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (uuid_visitante, datetime.datetime.now()))
                conn.commit()
                id_anonimo = cursor.lastrowid
        finally:
            conn.close()

        return {"id_anonimo": id_anonimo, "uuid": uuid_visitante}
