from datetime import datetime

class GeradorCodigo:
    @staticmethod
    def gerador_codigo_funcionario(id_usuarios: str, cpf: str,data_nascimento:str,cargo:str):
        # Adicionar a função para buscar as informações do funcionario

        cpf_limpo = cpf.replace('.','').replace('-','')
        cpf_primeiros = cpf_limpo[:3]

        data = datetime.strptime(data_nascimento, "%d/%m%y")
        mes_ano = data.strftime("%m%y")

        if cargo.upper().strip() == "GERENTE":
            nivel = "001"
        elif cargo.upper().strip() == "ATENDENTE":
            nivel = "002"
        elif cargo.upper().strip() == "ESTAGIARIO":
            nivel = "003"
        else:
            nivel = "004"

        return f"{cpf_primeiros}{mes_ano}{nivel}"