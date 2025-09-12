import pymysql

def get_db_connection():
	return pymysql.connect(
		host='localhost',
		user='manuelx6',
		password='Manueldev@.55',
		db='sing_technology',
		charset='utf8mb4',
		cursorclass=pymysql.cursors.DictCursor
	)
