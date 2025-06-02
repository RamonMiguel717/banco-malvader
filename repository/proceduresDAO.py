from conexao import DBContext

class Procedures:

    @staticmethod
    def generate_otp(id_usuario):
        with DBContext() as (_, cursor):
            cursor.callproc("gerar_otp",[id_usuario])
            for resultado in cursor.stored_results():
                otp = resultado.fetchone()
                return otp['novo_otp'] if otp else None
            
    @staticmethod
    def calc_score_credito(id_cliente):
        with DBContext() as (_, cursor):
            cursor.callproc("calc_score_credito",[id_cliente]) 