from utils.validator import Validator
from utils.criptografia_senha import criptografada
from repository.banco_dao import ClienteRepository,UsuarioRepository
from flask import jsonfy

class ClienteServices:

    @staticmethod
    def create_account(nome,cpf,data_nascimento,senha,telefone,email,tipo_usuario = 'cliente'):
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
        resultado_data = Validator.validate_idade()
        if not resultado_data['valido']:
            raise ValueError(f"Idade inválida: {resultado_data['erros']}")
    
        senha_hash = criptografada(senha)
        UsuarioRepository.insert_usuario(nome,cpf,data_nascimento,telefone,email,tipo_usuario,senha_hash,False,None)
        id_usuario = cursor
#Função inacabada
#TODO criar uma função para encontrar o id do usuário,funcionario,cliente e por ai vai.