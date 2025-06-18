import time

from banco_malvader.repository import banco_dao, tabelas_dao


def test_conexao():
    try:
        banco_dao.obter_conexao()
        print("✅ Conexão estabelecida")
    except Exception as e:
        print(f"❌ Falha na conexão: {e}")

def test_criar_banco():
    try:
        banco_dao.criar_banco()
        print("✅ Banco criado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar banco: {e}")

def test_criar_tabelas():
    try:
        banco_dao.criar_tabelas
        print("✅ Tabelas criadas com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")

def test_criar_banco_e_tabelas():
    try:
        banco_dao.criar_banco_e_tabelas()
        print("✅ Banco e tabelas criados com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar banco e tabelas: {e}")

def test_apagar_banco():
    try:
        banco_dao.apagar_banco()
        print("✅ Banco apagado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao apagar banco: {e}")

def test_apagar_tabelas():
    try:
        tabelas_dao.apagar_tabelas()
        print("✅ Tabelas apagadas com sucesso")
    except Exception as e:
        print(f"❌ Erro ao apagar tabelas: {e}")

def test_resetar_banco():
    test_apagar_tabelas()
    time.sleep(0.3)
    test_apagar_banco()
    time.sleep(0.3)
    test_criar_banco_e_tabelas()

def processo_completo():

    test_criar_banco() # Funciona
    time.sleep(0.3)
    test_conexao() # Funciona
    time.sleep(0.3)
    test_criar_tabelas() # Funciona
    time.sleep(0.3)
    test_apagar_tabelas()
    time.sleep(0.3)
    test_apagar_banco()
    time.sleep(0.3)
    test_criar_banco_e_tabelas()

if __name__ == '__main__':
    processo_completo()
    # Ou, se quiser somente resetar:
    # test_resetar_banco()
