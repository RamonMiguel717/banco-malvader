from repository.usuarioDAO import UsuarioRepository as usuario
from utils.validator import Validator
from utils.criptografia_senha import criptografada
from utils.exceptions import ValidacaoNegocioError, AcessoNegadoError

from datetime import datetime

class UsuarioServices:

    @staticmethod
    # Função de validação, identifica e formata o erro caso exista um.
    def _validar(label, resultado):
        if not resultado['valido']:
            raise ValidacaoNegocioError(f"{label} inválido: {resultado['erros']}")

    @staticmethod
    # Atualiza os dados do cliente a partir do parâmetro passado
    # Necessita de uma DECLARAÇÃO ESPECIFICA de qual informação irá ser atualizada
    # o unico parâmetro obrigatório é o id do usuário
    def atualizar_dados(id_usuario, telefone=None, email=None, senha=None):
        try:
            if telefone:
                UsuarioServices._validar("Telefone", Validator.validate_telefone(telefone))
            if email:
                UsuarioServices._validar("Email", Validator.validate_email(email))
            if senha:
                UsuarioServices._validar("Senha", Validator.validate_senha(senha))
                senha = criptografada(senha)

            usuario.update_usuario(id_usuario, telefone=telefone, email=email, senha_hash=senha)

            return {"status": "usuário atualizado"}
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao atualizar dados do usuário: {e}")

    @staticmethod
    # Função de autentificação de Login 
    def autenticar_usuario(cpf, senha):
        try:
            #Encontra as informações do usuário e as armazena em uma variavel para ser desempacotado depois
            usuario = usuario.get_usuario_by_cpf(cpf)
            if not usuario:
                raise AcessoNegadoError("Usuário não encontrado")

            senha_criptografada = criptografada(senha)
            if usuario["senha_hash"] != senha_criptografada:
                usuario.registrar_login(usuario["id_usuario"], sucesso=False)
                raise AcessoNegadoError("Senha incorreta")

            # TODO registrar login é uma função em integração com a auditoria -> Ainda não funciona
            usuario.registrar_login(usuario["id_usuario"], sucesso=True)
            return usuario

        except Exception as e:
            raise AcessoNegadoError(f"Erro de autenticação: {e}")

    @staticmethod
    def gerar_otp(id_usuario):
        try:
            return usuario.gerar_otp(id_usuario)
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao gerar OTP: {e}")

    @staticmethod
    def validar_otp(id_usuario, otp_digitado):
        try:
            if usuario.validar_otp(id_usuario, otp_digitado):
                return {"status": "OTP válido"}
            else:
                raise AcessoNegadoError("OTP inválido ou expirado")
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao validar OTP: {e}")

    @staticmethod
    def invalidar_otp(id_usuario):
        try:
            usuario.invalidar_otp(id_usuario)
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao invalidar OTP: {e}")

    @staticmethod
    def tentativas_invalidas_recentemente(id_usuario):
        try:
            total = usuario.tentativas_recentes_falhas(id_usuario)
            return total
        except Exception as e:
            raise ValidacaoNegocioError(f"Erro ao verificar tentativas inválidas: {e}")
