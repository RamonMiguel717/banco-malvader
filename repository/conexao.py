import mysql.connector
from dotenv import load_dotenv
from mysql.connector.cursor import MySQLCursorDict
import os

load_dotenv()

#Faz a conexão com o banco de dados e a criação do cursor

def obter_conexao():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

class DBContext:
    def __enter__(self):
        self.conn = obter_conexao()
        self.cursor = self.conn.cursor(cursor_class=MySQLCursorDict)
        return self.conn, self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()