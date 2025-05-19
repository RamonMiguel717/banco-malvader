from datetime import date
from pydantic import BaseModel,EmailStr,ValidationError

class EmailValidator(BaseModel):
    email: EmailStr

class Validator:
    @staticmethod
    def validate_nome(nome: str) -> bool:
        return nome.replace(" ", "").isalpha()
    
    @staticmethod
    def validate_cpf(cpf: str)-> bool:
        cpf =''.join(filter(str.isdigit,cpf))

        if len(cpf) != 11 or cpf == cpf[0]*11:
            return False
        soma = sum(int(cpf[i])* (10-i)for i in range(10))
        dig1 = (soma * 10 %11)% 10

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        dig2 = (soma * 10 % 11) % 10

        return cpf[-2:] == f"{dig1}{dig2}"

    @staticmethod
    def validate_idade(data_nascimento: int) -> bool:
#Não acho que esta classe aceite datas no modelo dd/mm/yyyy, devo mudar isso depois
        idade = date.today().year - data_nascimento
        return idade >=18
    @staticmethod
    def validate_email(email:str)-> bool:
        try:
            EmailValidator(email=email)
            return True
        except ValidationError:
            return False

        