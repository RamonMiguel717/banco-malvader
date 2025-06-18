from banco_malvader.conexao import DBContext

class Procedures:

    @staticmethod
    def criar_procedure_gerar_otp():
        sql =['DROP PROCEDURE IF EXISTS gerar_otp;',
        """CREATE PROCEDURE gerar_otp(IN id_usuario INT)
            BEGIN
            DECLARE novo_otp VARCHAR(6);
            SET novo_otp = LPAD(FLOOR(RAND() * 1000000), 6, '0');
            UPDATE usuario
            SET
                otp_codigo = novo_otp,
                otp_ativo = TRUE,
                otp_expiracao = NOW() + INTERVAL 5 MINUTE
            WHERE id_usuario = id_usuario;
            SELECT novo_otp AS otp;
        END;"""]
        with DBContext() as (_, cursor):
              for statement in sql:
                cursor.execute(statement)

  

    @staticmethod
    def criar_procedure_invalidar_otp():
        sql = ['DROP PROCEDURE IF EXISTS invalidar_otp;',
       """
        CREATE PROCEDURE invalidar_otp(IN id_usuario INT)
        BEGIN
            UPDATE usuario
            SET otp_ativo = FALSE,
                otp_codigo = NULL,
                otp_expiracao = NULL
            WHERE id_usuario = id_usuario;
        END;
    """]
        with DBContext() as (_, cursor):
            for statement in sql:
                cursor.execute(statement)
