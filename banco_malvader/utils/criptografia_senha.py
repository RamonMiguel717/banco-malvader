import bcrypt

class criptografada:

    def criptografar_senha(senha):
        senha_bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_bash = bcrypt.hashpw(senha_bytes,salt)

        return senha_bash

    def descript_senha(senha_bash,senha_inserida)-> bool:
        return bcrypt.checkpw(senha_inserida('utf-8'),senha_bash)
            

