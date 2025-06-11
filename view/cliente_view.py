def menu_cliente():
    print("\n === Menu Cliente === ")
    print("1 - Cadastrar Clientes ")
    print("2 - Listar Clientes ")
    opcao = input("Escolha uma opção: ")

    match opcao:
        case 1: 
            cadastro_clientes()
        case _: 
            print("Insert inválido")

def cadastro_clientes():
    print("\n === Menu de Cadastro ===")
    input("Nome completo: ")
    input("CPF: ")
    input("Data de nascimento: ")
