import pytest
from repository import usuario_dao
from model import usuario_model
from utils.criptografia_senha import criptografada


CPF_TESTE = "12345678900"
SENHA_TESTE = "senha123"


@pytest.fixture(scope="function")
def usuario_inserido():
    usuario = usuario_model.Usuario(
        nome="Ramon",
        cpf=CPF_TESTE,
        data_nascimento="2000-01-01",
        telefone="11999999999",
        email="teste@teste.com",
        tipo_usuario="CLIENTE",
        senha=criptografada(SENHA_TESTE),
        otp_ativo=False,
        otp_codigo=None
    )

    usuario_dao.UsuarioRepository.insert_usuario(
        nome=usuario.nome,
        cpf=usuario.cpf,
        data_nascimento=usuario.data_nascimento,
        telefone=usuario.telefone,
        email=usuario.email,
        tipo_usuario=usuario.tipo_usuario,
        senha_hash=usuario.senha_hash,
        otp_ativo=usuario.otp_ativo,
        otp_expiracao=None
    )
    yield usuario

    # Teardown (garante limpeza após teste)
    usuario_db = usuario_dao.UsuarioRepository.get_usuario_by_cpf(CPF_TESTE)
    if usuario_db:
        usuario_dao.UsuarioRepository.delete_usuario(usuario_db.id_usuario)
