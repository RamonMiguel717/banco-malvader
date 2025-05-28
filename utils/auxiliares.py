from datetime import datetime
import re


@staticmethod
def gerador_codigo_funcionario(id_usuarios: str, cpf: str,data_nascimento:str,cargo:str):
    # TODO Adicionar a função para buscar as informações do funcionario

    cpf_limpo = limpar_cpf(cpf)
    cpf_primeiros = cpf_limpo[:3]

    data = datetime.strptime(data_nascimento, "%d/%m%y")
    mes_ano = data.strftime("%m%y")

    if cargo.upper().strip() == "GERENTE":
        nivel = "001"
    elif cargo.upper().strip() == "ATENDENTE":
        nivel = "002"
    elif cargo.upper().strip() == "ESTAGIARIO":
        nivel = "003"
    else:
        nivel = "004"

    return f"{cpf_primeiros}{mes_ano}{nivel}"

@staticmethod   
def limpar_cpf(cpf:str):
    cpf_limpo =''.join(filter(str.isdigit, cpf))
    return cpf_limpo


@staticmethod 
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

@staticmethod # -> tira simbolos e espaços
def tratar_data(data: str) -> str:
    return re.sub(r'[^0-9]', '', data)

