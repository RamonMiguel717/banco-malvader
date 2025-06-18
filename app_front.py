import flet as ft
from banco_malvader.services.usuario_services import UsuarioServices
from banco_malvader.repository.usuario_dao import UsuarioRepository
from banco_malvader.services.cliente_services import ClienteServices
from banco_malvader.services import contas_services
from banco_malvader.utils.auxiliares import tratar_data


def main(page: ft.Page):
    page.title = "Banco Malvader"
    page.window_width = 400
    page.window_height = 500
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    dados_cliente = {
        "id_usuario": None,
        "nome": "",
        "cpf": "",
        "saldo": 0.0,
        "tipo_conta": "",
    }

    # Campos compartilhados
    nome_field = ft.TextField(label="Nome completo")
    cpf_field = ft.TextField(label="CPF")
    mensagem_login = ft.Text("")

    nome_cad = ft.TextField(label="Nome completo")
    cpf_cad = ft.TextField(label="CPF")
    senha_cad = ft.TextField(label="Senha", password=True, can_reveal_password=True)
    email_cad = ft.TextField(label="E-mail")
    telefone_cad = ft.TextField(label="Telefone")
    data_nascimento_cad = ft.TextField(label="Data de Nascimento (dd/mm/yyyy)")
    mensagem_cadastro = ft.Text("")

    otp_field = ft.TextField(label="Digite o código OTP enviado para seu email")
    mensagem_otp = ft.Text("")

    # ----------------- Funções das telas -----------------
    def rota(e):
        page.views.clear()

        # 🏁 Tela inicial
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Image(
                            src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Red_bank_icon.svg/512px-Red_bank_icon.svg.png",
                            width=150,
                            height=150,
                        ),
                        ft.Text("Banco Malvader", size=30, weight="bold"),
                        ft.Text("Seja bem-vindo!", size=20),
                        ft.ElevatedButton(
                            "Entrar como Cliente",
                            on_click=lambda _: page.go("/login"),
                        ),
                        ft.ElevatedButton(
                            "Cadastrar Novo Cliente",
                            on_click=lambda _: page.go("/cadastro"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # 🔐 Tela de login
        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.Text("Login", size=25, weight="bold"),
                        nome_field,
                        cpf_field,
                        ft.ElevatedButton("Enviar OTP", on_click=enviar_otp),
                        mensagem_login,
                        ft.TextButton(
                            "Voltar",
                            on_click=lambda _: page.go("/"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # 🆕 Tela de cadastro
        if page.route == "/cadastro":
            page.views.append(
                ft.View(
                    "/cadastro",
                    [
                        ft.Text("Cadastro de Cliente", size=25, weight="bold"),
                        nome_cad,
                        cpf_cad,
                        senha_cad,
                        telefone_cad,
                        email_cad,
                        data_nascimento_cad,
                        ft.ElevatedButton("Cadastrar", on_click=cadastrar_cliente),
                        mensagem_cadastro,
                        ft.TextButton(
                            "Voltar",
                            on_click=lambda _: page.go("/"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # 🔑 Tela OTP
        if page.route == "/otp":
            page.views.append(
                ft.View(
                    "/otp",
                    [
                        ft.Text("Validação de OTP", size=25, weight="bold"),
                        otp_field,
                        ft.ElevatedButton("Validar", on_click=validar_otp),
                        mensagem_otp,
                        ft.TextButton(
                            "Voltar",
                            on_click=lambda _: page.go("/login"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # 🏦 Tela Home do Cliente
        if page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    [
                        ft.Text(f"Olá, {dados_cliente['nome']}", size=22, weight="bold"),
                        ft.Text(f"CPF: {dados_cliente['cpf']}"),
                        ft.Text(f"Tipo de conta: {dados_cliente['tipo_conta']}"),
                        ft.Text(
                            f"Saldo: R$ {dados_cliente['saldo']:.2f}",
                            size=20,
                            weight="bold",
                            color="green",
                        ),
                        ft.Divider(),
                        ft.ElevatedButton(
                            "Ver Extrato",
                            on_click=lambda _: ft.alert_dialog("Extrato ainda não implementado"),
                        ),
                        ft.TextButton(
                            "Sair",
                            on_click=lambda _: page.go("/"),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        page.update()

    # ----------------- Ações -----------------

    def enviar_otp(e):
        nome = nome_field.value.strip()
        cpf = cpf_field.value.strip()

        if nome and cpf:
            try:
                user = UsuarioRepository.get_usuario_by_cpf(cpf)

                if user and user.nome.lower() == nome.lower():
                    dados_cliente["id_usuario"] = user.id_usuario
                    dados_cliente["nome"] = user.nome
                    dados_cliente["cpf"] = user.cpf

                    UsuarioServices.gerar_e_enviar_otp(user.id_usuario)

                    mensagem_login.value = "OTP enviado para seu e-mail."
                    page.go("/otp")
                else:
                    mensagem_login.value = "Nome ou CPF inválidos."
                    page.update()

            except Exception as err:
                mensagem_login.value = f"Erro: {err}"
                page.update()
        else:
            mensagem_login.value = "Preencha todos os campos!"
            page.update()

    def validar_otp(e):
        otp = otp_field.value.strip()

        if UsuarioServices.validar_otp(dados_cliente["id_usuario"], otp):
            try:
                mensagem_otp.value = ""
                tela_sem_conta()  # chamada direta à função, renderiza a tela
            except Exception as err:
                mensagem_otp.value = f"Erro ao buscar conta: {err}"
                page.update()
        else:
            mensagem_otp.value = "Código OTP inválido."
            page.update()

    def cadastrar_cliente(e):
        nome = nome_cad.value.strip()
        cpf = cpf_cad.value.strip()
        senha = senha_cad.value.strip()
        email = email_cad.value.strip()
        telefone = telefone_cad.value.strip()
        data_nascimento = data_nascimento_cad.value.strip()

        if nome and cpf and senha and email and telefone and data_nascimento:
            try:
                ClienteServices.create_account(
                    nome=nome,
                    cpf=cpf,
                    senha=senha,
                    telefone=telefone,
                    email=email,
                    data_nascimento=tratar_data(data_nascimento)
                )
                mensagem_cadastro.value = "Cadastro realizado com sucesso!"
                mensagem_cadastro.color = "green"
                page.update()
                page.go("/")  # 🔥 Volta para página inicial
            except Exception as err:
                mensagem_cadastro.value = f"Erro no cadastro: {err}"
                mensagem_cadastro.color = "red"
                page.update()
        else:
            mensagem_cadastro.value = "Preencha todos os campos!"
            mensagem_cadastro.color = "red"
            page.update()

    # ----------------- Inicialização -----------------
    page.on_route_change = rota
    page.go("/")  # Começa na tela inicial

    # ---------------- Tela pós validação OTP (sem conta criada) ---------------
 # ---------------- Tela de criação de conta --------------------
    tipo_conta_field = ft.Dropdown(
        label="Tipo de Conta",
        options=[
            ft.dropdown.Option(text="Corrente", key="CORRENTE"),
            ft.dropdown.Option(text="Poupança", key="POUPANCA"),
            ft.dropdown.Option(text="Investimento", key="INVESTIMENTO"),
        ],
    )

    agencia_field = ft.Dropdown(
        label="Agência",
        options=[
            ft.dropdown.Option(text="Banco do Brasil (001)", key="001"),
            ft.dropdown.Option(text="Banco Central (002)", key="002"),
            ft.dropdown.Option(text="Banco Bradesco (003)", key="003"),
        ],
    )

    msg_criacao_conta = ft.Text("")

    def criar_conta(e):
        tipo = tipo_conta_field.value  # "CORRENTE", "POUPANCA", "INVESTIMENTO"
        id_agencia = agencia_field.value  # "001", "002", "003"
        id_cliente = dados_cliente["id_usuario"]

        try:
            if tipo == "CORRENTE":
                contas_services.ContaCorrenteService.criar_conta_corrente(id_agencia, id_cliente)

            elif tipo == "POUPANCA":
                contas_services.ContaPoupancaService.criar_conta_poupanca(id_agencia, id_cliente)

            elif tipo == "INVESTIMENTO":
                # Esses valores poderiam vir da interface (por enquanto fixos)
                perfil_risco = "MODERADO"
                valor_minimo = 1000.0
                taxa_rendimento_base = 1.2
                contas_services.ContaInvestimentoService.criar_conta_investimento(
                    id_agencia, id_cliente, perfil_risco, valor_minimo, taxa_rendimento_base
                )
            else:
                raise ValueError("Tipo de conta inválido.")

            msg_criacao_conta.value = "Conta criada com sucesso!"
            msg_criacao_conta.color = "green"
            tela_pagina_inicial()

        except Exception as err:
            msg_criacao_conta.value = f"Erro: {err}"
            msg_criacao_conta.color = "red"

        page.update()

    def tela_criacao_conta():
        page.views.append(
            ft.View(
                "/criar_conta",
                [
                    ft.Text("Criar Nova Conta", size=25, weight="bold"),
                    tipo_conta_field,
                    agencia_field,  # <-- estava faltando aqui
                    ft.ElevatedButton("Confirmar", on_click=criar_conta),
                    msg_criacao_conta,
                    ft.TextButton("Voltar", on_click=lambda _: page.go("/sem_conta")),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()

    def tela_sem_conta():
        page.views.append(
            ft.View(
                "/sem_conta",
                [
                    ft.Text("Você ainda não possui conta bancária.", size=20),
                    ft.ElevatedButton("Criar Conta", on_click=lambda _: tela_criacao_conta()),
                    ft.TextButton("Voltar", on_click=lambda _: page.go("/")),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()


    # ---------------- Interface de perfil do usuário -------------------
    def tela_perfil():
        page.views.append(
            ft.View(
                "/perfil",
                [
                    ft.Text("Perfil do Usuário", size=25, weight="bold"),
                    ft.Text(f"Nome: {dados_cliente['nome']}"),
                    ft.Text(f"CPF: {dados_cliente['cpf']}"),
                    ft.TextButton("Voltar", on_click=lambda _: page.go("/home")),
                ]
            )
        )
        page.update()

    # ---------------- Interface de Depósito --------------------
    deposito_field = ft.TextField(label="Valor para depósito", keyboard_type=ft.KeyboardType.NUMBER)
    mensagem_deposito = ft.Text("")

    def realizar_deposito(e):
        valor = float(deposito_field.value)
        try:
            contas_services.ContaService.depositar(dados_cliente["id_usuario"], valor)
            dados_cliente["saldo"] += valor
            mensagem_deposito.value = "Depósito realizado com sucesso!"
            mensagem_deposito.color = "green"
            page.go("/home")
        except Exception as err:
            mensagem_deposito.value = f"Erro: {err}"
            mensagem_deposito.color = "red"
        page.update()

    def tela_deposito():
        page.views.append(
            ft.View(
                "/deposito",
                [
                    ft.Text("Depósito", size=25, weight="bold"),
                    deposito_field,
                    ft.ElevatedButton("Depositar", on_click=realizar_deposito),
                    mensagem_deposito,
                    ft.TextButton("Voltar", on_click=lambda _: page.go("/home")),
                ]
            )
        )
        page.update()

    # ---------------- Interface de Extrato --------------------
    def tela_extrato():
        extrato = contas_services.ContaService.obter_extrato(dados_cliente["id_usuario"])
        extrato_list = [
            ft.Text(f"{mov.data} - {mov.tipo} - R$ {mov.valor:.2f}") for mov in extrato
        ] or [ft.Text("Nenhuma movimentação encontrada.")]

        page.views.append(
            ft.View(
                "/extrato",
                [
                    ft.Text("Extrato da Conta", size=25, weight="bold"),
                    ft.Column(extrato_list),
                    ft.TextButton("Voltar", on_click=lambda _: page.go("/home")),
                ]
            )
        )
        page.update()

    # Atualize a tela inicial (página do cliente) para incluir os novos botões
    def tela_pagina_inicial():
        page.views.append(
            ft.View(
                "/home",
                [
                    ft.Text(f"Olá, {dados_cliente['nome']}", size=22, weight="bold"),
                    ft.Text(f"CPF: {dados_cliente['cpf']}"),
                    ft.Text(f"Tipo de conta: {dados_cliente['tipo_conta']}"),
                    ft.Text(f"Saldo: R$ {dados_cliente['saldo']:.2f}", size=20, weight="bold", color="green"),
                    ft.Divider(),
                    ft.ElevatedButton("Ver Extrato", on_click=lambda _: tela_extrato()),
                    ft.ElevatedButton("Depositar", on_click=lambda _: tela_deposito()),
                    ft.ElevatedButton("Perfil", on_click=lambda _: tela_perfil()),
                    ft.TextButton("Sair", on_click=lambda _: page.go("/")),
                ]
            )
        )
        page.update()

ft.app(target=main)
