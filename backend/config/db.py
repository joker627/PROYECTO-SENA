import os
﻿import pymysql

def get_db_connection():
	return pymysql.connect(
		host=os.environ.get('DB_HOST', 'localhost'),
		user=os.environ.get('DB_USER', ''),
		password=os.environ.get('DB_PASSWORD', ''),
		db=os.environ.get('DB_NAME', ''),
		charset='utf8mb4',
		cursorclass=pymysql.cursors.DictCursor
	)
