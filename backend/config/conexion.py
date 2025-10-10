# ===== CONFIGURACIÓN PARA DB=====
# detecta estos nombres y los reemplaza
import os
MYSQLHOST = os.environ['MYSQLHOST'] 
MYSQLUSER = os.environ['MYSQLUSER']
MYSQLPASSWORD = os.environ['MYSQLPASSWORD']
MYSQLDATABASE = os.environ['MYSQLDATABASE']
MYSQLPORT = int(os.environ['MYSQLPORT'])
MYSQLCHARSET = 'utf8mb4'
