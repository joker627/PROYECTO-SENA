import pymysql
from .conexion import MYSQLHOST, MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE, MYSQLPORT, MYSQLCHARSET

def get_db_connection():
    print(f"🔧 Debug - MYSQLHOST: {MYSQLHOST}")  # Ver qué valor tiene
    print(f"🔧 Debug - MYSQLUSER: {MYSQLUSER}")
    
    return pymysql.connect(
        host=MYSQLHOST,
        user=MYSQLUSER,
        password=MYSQLPASSWORD,
        db=MYSQLDATABASE,
        port=MYSQLPORT,
        charset=MYSQLCHARSET,
        cursorclass=pymysql.cursors.DictCursor
    )
