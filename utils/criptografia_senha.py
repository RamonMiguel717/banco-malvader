import bcrypt

class criptografada:

    @staticmethod
    def criptografar_senha(senha):
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt)
        return senha_hash

    @staticmethod
    def descript_senha(senha_hash, senha_inserida):
        return bcrypt.checkpw(senha_inserida.encode('utf-8'), senha_hash)
