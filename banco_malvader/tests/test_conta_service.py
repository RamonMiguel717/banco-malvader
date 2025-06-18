import pytest
from banco_malvader.services.cliente_services import ClienteServices
from banco_malvader.services.contas_services import ContaService,ContaCorrenteService
from banco_malvader.repository.contas_dao import ContaRepository as CT


def test_criacao_de_conta():
    resultado = ClienteServices.create_account(
        nome="Teste Cliente",
        cpf="12345678901",
        data_nascimento="1990-01-01",
        senha="Senha123",
        telefone="11999999999",
        email="teste@email.com"
    )
    assert resultado["status"] == "sucesso"
    assert resultado["id_usuario"] is not None


def test_criar_conta_base_e_corrente():
    id_cliente = 1
    numero = ContaService.criar_conta_base(1, "CORRENTE", id_cliente)

    conta = next((c for c in CT.list_contas() if c.numero_conta == numero), None)
    assert conta is not None
    assert conta.status == "ATIVA"

    ContaCorrenteService.criar_conta_corrente(conta.id_conta, id_cliente)
    dados_corrente = ContaService.consultar_status(conta.id_conta)
    assert dados_corrente["tipo_conta"] == "CORRENTE"


def test_deposito():
    conta = CT.list_contas()[0]
    saldo_anterior = conta.saldo

    resultado = ContaService.depositar(conta.id_conta, 500)
    assert resultado["sucesso"] is True
    assert resultado["novo_saldo"] == saldo_anterior + 500


def test_saque():
    conta = CT.list_contas()[0]
    saldo_anterior = conta.saldo

    resultado = ContaCorrenteService.realizar_saque(conta.id_conta, conta.id_agencia, 100)
    assert resultado["sucesso"] is True
    assert resultado["novo_saldo"] == saldo_anterior - 100


def test_transferencia():
    contas = CT.list_contas()
    origem = contas[0]
    destino = contas[1] if len(contas) > 1 else None

    if not destino:
        # Criar uma conta destino se não existir
        numero = ContaService.criar_conta_base(1, "CORRENTE", 1)
        destino = next((c for c in CT.list_contas() if c.numero_conta == numero), None)
        ContaCorrenteService.criar_conta_corrente(destino.id_conta, 1)

    saldo_origem = origem.saldo
    saldo_destino = destino.saldo

    resultado = ContaService.transferir(origem.id_conta, destino.id_conta, 50)
    assert resultado["sucesso"] is True
    assert resultado["novo_saldo_origem"] == saldo_origem - 50
    assert resultado["novo_saldo_destino"] == saldo_destino + 50


def test_consultar_saldo():
    conta = CT.list_contas()[0]
    saldo = ContaService.consultar_status(conta.id_conta)["saldo"]
    assert saldo >= 0


def test_encerrar_e_reativar_conta():
    conta = CT.list_contas()[0]
    resultado_encerrar = ContaService.encerrar_conta(conta.id_conta)
    assert resultado_encerrar["sucesso"] is True

    dados = ContaService.consultar_status(conta.id_conta)
    assert dados["status"] == "ENCERRADA"

    resultado_reativar = ContaService.reativar_conta(conta.id_conta)
    assert resultado_reativar["sucesso"] is True

    dados = ContaService.consultar_status(conta.id_conta)
    assert dados["status"] == "ATIVA"
