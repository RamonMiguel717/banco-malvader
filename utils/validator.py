from datetime import date, datetime
from pydantic import BaseModel, EmailStr, ValidationError
from utils import auxiliares
import re

class EmailValidator(BaseModel):
    email: EmailStr

class Validator:
    @staticmethod
    def validate_nome(nome: str) -> dict:
        erros = []
        if not nome.replace(" ", "").isalpha():
            erros.append("O nome deve conter apenas letras.")
        return {"valido": len(erros) == 0, "erros": erros}

    @staticmethod
    def validate_cpf(cpf: str) -> dict:
        erros = []
        cpf = auxiliares.limpar_cpf(cpf)

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            erros.append("CPF inválido.")
        else:
            soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
            dig1 = (soma * 10 % 11) % 10

            soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
            dig2 = (soma * 10 % 11) % 10

            if cpf[-2:] != f"{dig1}{dig2}":
                erros.append("CPF inválido.")

        return {"valido": len(erros) == 0, "erros": erros}

    @staticmethod
    def validate_idade(data_nascimento_str: str) -> dict:
        erros = []
        try:
            data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y").date()
            hoje = date.today()
            idade = hoje.year - data_nascimento.year - (
                (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
            )
            if idade < 18:
                erros.append("É necessário ter 18 anos ou mais.")
        except ValueError:
            erros.append("Data de nascimento inválida. Use o formato dd/mm/yyyy.")
        return {"valido": len(erros) == 0, "erros": erros}

    @staticmethod
    def validate_email(email: str) -> dict:
        erros = []
        try:
            EmailValidator(email=email)
        except ValidationError:
            erros.append("E-mail inválido.")
        return {"valido": len(erros) == 0, "erros": erros}

    @staticmethod
    def validate_senha(senha: str, email: str, nome: str, data_nascimento: date) -> dict:
        erros = []

        if len(senha) < 8:
            erros.append("A senha deve ter no mínimo 8 caracteres.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            erros.append("A senha deve conter pelo menos um caractere especial.")
        if not re.search(r"[a-z]", senha):
            erros.append("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r"[A-Z]", senha):
            erros.append("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[0-9]", senha):
            erros.append("A senha deve conter pelo menos um número.")
        if auxiliares.verificar_sequencia_numerica(senha):
            erros.append("A senha não pode conter sequência numérica.")

        nome_formatado = re.sub(r'\s+', '', nome.lower())
        if nome_formatado and nome_formatado in senha.lower():
            erros.append("A senha não pode conter seu nome.")

        if email and email.split("@")[0].lower() in senha.lower():
            erros.append("A senha não pode conter seu e-mail.")

        # Correção aqui
        data_str = data_nascimento.strftime("%d/%m/%Y")
        data_formatada = auxiliares.tratar_data(data_str)

        if data_formatada in senha:
            erros.append("A senha não pode conter sua data de nascimento.")

        return {"valido": len(erros) == 0, "erros": erros}


    @staticmethod
    def validate_telefone(telefone:str)-> dict:
        erros = []
        telefone_limpo = re.sub(r'\D','',telefone)
        if not telefone_limpo.isdigit():
            erros.append("O campo telefone não aceita letras")
        if len(telefone_limpo) == 10:
            erros.append("O numero deve conter o DDD")
        return {"valido": len(erros) == 0,"erros":erros}