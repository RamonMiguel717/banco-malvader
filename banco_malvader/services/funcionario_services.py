from banco_malvader.model.funcionario_model import Funcionario
from banco_malvader.repository.funcionario_dao import FuncionarioRepository
from banco_malvader.repository.usuario_dao import UsuarioRepository
from banco_malvader.utils.exceptions import ValidacaoNegocioError


class FuncionarioServices:

    @staticmethod
    def criar_funcionario(id_usuario: int, cargo: str, id_supervisor: int | None = None) -> int:
        """
        Cria um novo funcionário e gera seu código automaticamente.
        """

        if not UsuarioRepository.get_usuario_by_id(id_usuario):
            raise ValidacaoNegocioError("Usuário não encontrado para vincular ao funcionário.")

        funcionario_existente = FuncionarioRepository.get_funcionario_by_id(id_usuario)
        if funcionario_existente:
            raise ValidacaoNegocioError("Este usuário já está cadastrado como funcionário.")

        novo_funcionario = Funcionario(
            id_funcionario=None,
            id_usuario=id_usuario,
            codigo_funcionario=None,  # será gerado no DAO
            cargo=cargo.upper().strip(),
            id_supervisor=id_supervisor
        )

        FuncionarioRepository.insert_funcionario(novo_funcionario)

        funcionario = FuncionarioRepository.get_funcionario_by_id(id_usuario)
        return funcionario.id_funcionario

    @staticmethod
    def buscar_funcionario_por_id(id_usuario: int) -> Funcionario:
        funcionario = FuncionarioRepository.get_funcionario_by_id(id_usuario)
        if not funcionario:
            raise ValidacaoNegocioError("Funcionário não encontrado.")
        return funcionario

    @staticmethod
    def buscar_funcionario_por_cpf(cpf: str) -> Funcionario:
        id_funcionario = FuncionarioRepository.find_funcionario_id_by_cpf(cpf)
        if not id_funcionario:
            raise ValidacaoNegocioError("Funcionário não encontrado para o CPF fornecido.")
        funcionario = FuncionarioRepository.get_funcionario_by_id(id_funcionario)
        return funcionario

    @staticmethod
    def listar_funcionarios() -> list[Funcionario]:
        return FuncionarioRepository.list_funcionarios()

    @staticmethod
    def atualizar_funcionario(funcionario: Funcionario):
        """
        Atualiza os dados de um funcionário.
        """
        funcionario_existente = FuncionarioRepository.get_funcionario_by_id(funcionario.id_usuario)
        if not funcionario_existente:
            raise ValidacaoNegocioError("Funcionário não encontrado para atualização.")

        funcionario.id_funcionario = funcionario_existente.id_funcionario
        FuncionarioRepository.atualizar_funcionario(funcionario)

    @staticmethod
    def excluir_funcionario(id_funcionario: int):
        funcionario = next(
            (f for f in FuncionarioRepository.list_funcionarios() if f.id_funcionario == id_funcionario),
            None
        )
        if not funcionario:
            raise ValidacaoNegocioError("Funcionário não encontrado para exclusão.")
        
        FuncionarioRepository.delete_funcionario(id_funcionario)
