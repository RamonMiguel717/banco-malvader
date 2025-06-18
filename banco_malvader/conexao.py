from mysql.connector import connect
from dotenv import load_dotenv
import os

load_dotenv()

def obter_conexao():
    return connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "senha"),
        database=os.getenv("DB_DATABASE", "banco_malvader"),
        port=int(os.getenv("DB_PORT", "3306"))
    )

class DBContext:
    def __enter__(self):
        self.conn = obter_conexao()
        self.cursor = self.conn.cursor(dictionary=True)  # ← SIMPLES, LIMPO, FUNCIONAL
        return self.conn, self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()