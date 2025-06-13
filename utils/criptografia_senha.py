import bcrypt

class criptografada:

    @staticmethod
    def gerar_hash_senha(senha: str) -> str:
        """Gera um hash seguro para a senha usando bcrypt."""
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt)
        return senha_hash.decode('utf-8')  # salva como string no banco

    @staticmethod
    def verificar_senha(senha_hash: str, senha_inserida: str) -> bool:
        """Verifica se a senha inserida confere com o hash armazenado."""
        return bcrypt.checkpw(senha_inserida.encode('utf-8'), senha_hash.encode('utf-8'))
