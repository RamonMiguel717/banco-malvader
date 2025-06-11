from datetime import datetime, date
from repository.usuarioDAO import get_usuario_by_id
from repository.contasDAO import ContaRepository as conta, ContaCorrenteRepository as CC
from dateutil import relativedelta
import random
import re

# TODO adicionar validações ao codigo, além da trataiva de erros

"""
O codigo do funcionário é uma combinação das informações pessoais do funcionário além do seu cargo dentro do Banco
"""
def gerador_codigo_funcionario(id_usuario: str, cargo):
    usuario = get_usuario_by_id(id_usuario)
    cpf = usuario['cpf']
    data_nascimento = usuario['data_nascimento']

    cpf_limpo = limpar_cpf(cpf)
    cpf_primeiros = cpf_limpo[:3]

    # Garantir que data esteja no formato datetime
    if isinstance(data_nascimento, str):
        data = datetime.strptime(data_nascimento, "%Y-%m-%d")
    else:
        data = data_nascimento

    mes_ano = data.strftime("%m%y")

    # Código por cargo
    cargo = cargo.upper().strip()
    if cargo == "GERENTE":
        nivel = "001"
    elif cargo == "ATENDENTE":
        nivel = "002"
    elif cargo == "ESTAGIARIO":
        nivel = "003"
    else:
        nivel = "004"

    return f"{cpf_primeiros}{mes_ano}{nivel}"

# Tira qualquer informação não numérica do CPF inserido 
def limpar_cpf(cpf:str):
    cpf_limpo =''.join(filter(str.isdigit, cpf))
    return cpf_limpo


 # Parte das funções de validação de senha, identifica caso exista uma sequência numérica (123,321,432,987...)
def verificar_sequencia_numerica(senha,tamanho_min = 1):
    numeros = ''.join(filter(str.isdigit,senha))
    if len(numeros) < tamanho_min:
        return False
    
    for i in range(len(numeros)-tamanho_min + 1):
        trecho = numeros[i:i +tamanho_min]
        if trecho.isdigit():
            digitos = list(map(int, trecho))

            crescente = all(digitos[i]+1 == digitos[i+1] for i in range(len(digitos)-1))
            decrescente = all(digitos[i] -1 == digitos[i+1] for i in range(len(digitos)-1))

            if crescente or decrescente:
                return True
    return True

 # -> tira simbolos e espaços da data
def tratar_data(data: str) -> str:
    for formato in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d%m%Y"):
        try:
            return datetime.strptime(data, formato).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Formato de data inválido: {data}")


def gerar_numero_conta():
    # Gera um número base com 8 dígitos
    numero_base = ''.join(str(random.randint(0, 9)) for _ in range(8))
    digito = calcular_digito_luhn(numero_base)
    return f"{numero_base}-{digito}"
# É uma das camadas de segurança requerida no documento
def calcular_digito_luhn(numero_str):
    soma = 0
    reverso = numero_str[::-1]
    for i, char in enumerate(reverso):
        n = int(char)
        if i % 2 == 0:
            n *= 2
            if n > 9:
                n -= 9
        soma += n
    digito = (10 - (soma % 10)) % 10
    return str(digito)

# Calcula o limite da conta
def calcular_limite_por_score(score):
    if score >= 90:
        return 5000.00
    elif score >= 70:
        return 2000.00
    elif score >= 50:
        return 1000.00
    else:
        return 500.00

def calcular_data_vencimento(data_ultima_transaacao: date):
    return data_ultima_transaacao + relativedelta(months = 6)

def atualizar_data_vencimento(id_conta):
    try:
        data_ultima = conta.get_data_ultima_transacao(id_conta)
        if not data_ultima:
            return

        nova_data = calcular_data_vencimento(data_ultima.date())
        CC.update_data_vencimento(id_conta,nova_data)
    except Exception as e:
        raise Exception(f"Não foi possível atualizar a data de vencimento:{e}")