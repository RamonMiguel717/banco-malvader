from repository import banco_dao
from repository import conexao

if __name__ == '__main__':
        
    banco_dao.criar_banco()
    conexao.obter_conexao()
    banco_dao.criar_tabelas()
    