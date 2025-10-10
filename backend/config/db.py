import pymysql
import os

def get_db_connection():
    return pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        db=os.environ['DB_NAME'],
        port=int(os.environ['DB_PORT']),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
