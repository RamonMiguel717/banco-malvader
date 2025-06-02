from utils.validator import Validator
from utils.criptografia_senha import criptografada
from repository import usuarioDAO as usuario, clienteDAO as Cliente
from repository.contasDAO import ContaCorrenteRepository as CC, ContaInvestimentoRepository as CI, ContaPoupancaRepository as CP, ContaRepository as conta

class ClienteServices:

    @staticmethod
    def create_account(nome, cpf, data_nascimento, senha, telefone, email, tipo_usuario='CLIENTE'):
        resultado_nome = Validator.validate_nome(nome)
        if not resultado_nome["valido"]:
            raise ValueError(f"Nome inválido: {resultado_nome['erros']}")

        resultado_cpf = Validator.validate_cpf(cpf)
        if not resultado_cpf["valido"]:
            raise ValueError(f"CPF inválido: {resultado_cpf['erros']}")

        resultado_senha = Validator.validate_senha(senha)
        if not resultado_senha['valido']:
            raise ValueError(f"Senha Inválida: {resultado_senha['erros']}")

        resultado_telefone = Validator.validate_telefone(telefone)
        if not resultado_telefone['valido']:
            raise ValueError(f"Telefone inválido: {resultado_telefone['erros']}")

        resultado_email = Validator.validate_email(email)
        if not resultado_email['valido']:
            raise ValueError(f"Email inválido: {resultado_email['erros']}")

        resultado_data = Validator.validate_idade(data_nascimento)
        if not resultado_data['valido']:
            raise ValueError(f"Idade inválida: {resultado_data['erros']}")

        senha_hash = criptografada(senha)
        usuario.insert_usuario(nome, cpf, data_nascimento, telefone, email, tipo_usuario, senha_hash, False, None)

        id_usuario = usuario.get_usuario_by_cpf(cpf)['id_usuario']
        Cliente.insert_cliente(id_usuario)

        return {"status": "sucesso", "id_usuario": id_usuario}

    def get_cliente_by_usuario(id_usuario):
        try:
            cliente = Cliente.get_cliente_by_id(id_usuario)
            contas = conta.get_contas_by_cliente(cliente['id_cliente'])
            score = cliente['score_credito']
            return {
                'cliente': cliente,
                'contas': contas,
                'score': score
            }
        except Exception as e:
            print(f"Erro ao identificar cliente: {e}")

    def get_cliente_by_cpf(cpf):
        clientes = Cliente.get_cliente_by_cpf(cpf)
        contas = conta.get_contas_by_cliente(clientes['id_cliente'])
        score = clientes['score_credito']
        return {
            'cliente': clientes,
            'contas': contas,
            'score': score
        }

    def get_contas_do_cliente(id_cliente):
        contas = conta.get_contas_by_cliente(id_cliente)
        return contas
    

    def list_clientes():
        try:
            clientes_cru = Cliente.listar_clientes_completo()
            clientes_formatados = []

            for cliente in clientes_cru:
                clientes_formatados.append({
                    "id_cliente": cliente["id_cliente"],
                    "nome": cliente["nome"],
                    "cpf": cliente["cpf"],
                    "score_credito": cliente["score_credito"]
                })

            return clientes_formatados

        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []

