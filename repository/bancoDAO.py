def criar_banco_e_tabelas():
    from repository.tabelasDAO import Tabelas as T
    from repository.proceduresDAO import Procedures 

    try:
        criar_banco()

        # Criação de tabelas
        T.create_table_usuario()
        T.create_table_funcionarios()
        T.create_table_cliente()
        T.create_table_endereco()
        T.create_table_agencia()
        T.create_table_conta()
        T.create_table_conta_poupanca()
        T.create_table_conta_corrente()
        T.create_table_conta_investimentos()
        T.create_table_transacao()
        T.create_table_auditoria()
        T.create_table_relatorio()


        Procedures.criar_procedure_gerar_otp()
        Procedures.criar_procedure_invalidar_otp()

    except mysql.connector.Error as err:
        tratar_erro_mysql(err)


# TODO: Criar uma função para apagar tudo do banco de dados

