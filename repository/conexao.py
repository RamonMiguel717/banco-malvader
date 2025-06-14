import mysql.connector
from dotenv import load_dotenv
from mysql.connector.cursor import MySQLCursorDict
import os

load_dotenv()
#Funciona
def obter_conexao():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "nova_senha"),
        database="banco_malvader",
        port=int(os.getenv("DB_PORT", 3306))
    )


class DBContext:
    def __enter__(self):
        self.conn = obter_conexao()
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        #self.cursor.close()
        #self.conn.close()

