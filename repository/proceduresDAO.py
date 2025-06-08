from conexao import DBContext


"""
TODO devo rever esta classe, está redundante.

O objetivo dela é fazer a chamada de funções que executem as procedures dentro do banco de dados, entretanto,
como as procedures são ações de cada objeto faz mais sentido colocar cada procedure em seu próprio objeto(FUNCIONARIO,USUARIO,CLIENTE...)
"""

class Procedures:
        
    @staticmethod
    def calc_score_credito(id_cliente):
        with DBContext() as (_, cursor):
            cursor.callproc("calc_score_credito",[id_cliente]) 