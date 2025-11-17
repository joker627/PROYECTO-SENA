import pymysql
from pymysql import Error
from web.config.conexion import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )
    
def test_connection():
    try:
        connection = get_db_connection()
        print("Conexión a la base de datos exitosa")
    except Error as e:
        print(f"El error '{e}' ocurrió al conectar a la base de datos")
    return connection
