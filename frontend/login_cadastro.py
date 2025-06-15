import sys
from flet import Colors
from pathlib import Path

# Adiciona o diretório raiz ao sys.path para importar backend, etc
sys.path.append(str(Path(__file__).resolve().parents[1]))

import flet as ft
from datetime import datetime
from backend.utils.auxiliares import Auxiliares
from backend.utils.validator import Validator
from backend.utils.criptografia_senha import criptografada
from backend.repository.usuarioDAO import UsuarioRepository

def login_cadastro_page(page: ft.Page):
    page.title = "Banco Malvader - Login/Cadastro"
    page.session.set("cpf", None)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # CAMPOS DE LOGIN
    login_cpf = ft.TextField(label="CPF", width=300)
    login_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    login_msg = ft.Text(value="", color=ft.Colors.RED, size=12)

    # CAMPOS DE CADASTRO
    nome = ft.TextField(label="Nome completo", width=300)
    cpf = ft.TextField(label="CPF", width=300)
    data_nasc = ft.TextField(label="Data de nascimento (dd/mm/aaaa)", width=300)
    telefone = ft.TextField(label="Telefone", width=300)
    email = ft.TextField(label="Email", width=300)
    tipo_usuario = ft.Dropdown(
        label="Tipo de usuário",
        options=[
            ft.dropdown.Option("cliente"),
            ft.dropdown.Option("funcionario")
        ],
        width=300
    )
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    cadastro_msg = ft.Text(value="", color=ft.Colors.RED, size=12)

    # Função de login
    def realizar_login(e):
        login_msg.value = ""
        page.update()

        cpf_formatado = Auxiliares.limpar_cpf(login_cpf.value)
        usuario = UsuarioRepository.get_usuario_by_cpf(cpf_formatado)

        if not usuario:
            login_msg.value = "CPF não cadastrado."
        elif not criptografada.verificar_senha(usuario.senha_hash, login_senha.value):
            login_msg.value = "Senha incorreta."
            UsuarioRepository.registrar_login(usuario.id_usuario, sucesso=False)
        else:
            UsuarioRepository.registrar_login(usuario.id_usuario, sucesso=True)
            page.session.set("cpf", usuario.cpf)

            otp = Auxiliares.gerar_otp(usuario.cpf)
            print(f"[DEBUG] OTP gerado: {otp}")  # Apenas para teste

            page.go("/validar_otp")
        page.update()

    # Função de cadastro
    def realizar_cadastro(e):
        cadastro_msg.value = ""
        page.update()

        erros = []
        nome_val = Validator.validate_nome(nome.value)
        cpf_val = Validator.validate_cpf(cpf.value)
        idade_val = Validator.validate_idade(data_nasc.value)
        email_val = Validator.validate_email(email.value)
        tel_val = Validator.validate_telefone(telefone.value)

        try:
            data_formatada = datetime.strptime(data_nasc.value, "%d/%m/%Y").date()
        except ValueError:
            data_formatada = None
            idade_val = {"valido": False, "erros": ["Data de nascimento inválida. Use o formato dd/mm/yyyy."]}

        senha_val = Validator.validate_senha(
            senha.value,
            email.value,
            nome.value,
            data_formatada or datetime.today()
        )

        for val in [nome_val, cpf_val, idade_val, email_val, tel_val, senha_val]:
            if not val["valido"]:
                erros.extend(val["erros"])

        if UsuarioRepository.get_usuario_by_cpf(Auxiliares.limpar_cpf(cpf.value)):
            erros.append("CPF já cadastrado.")

        if erros:
            cadastro_msg.value = "\n".join(erros)
            page.update()
            return

        senha_hash = criptografada.gerar_hash_senha(senha.value)

        UsuarioRepository.insert_usuario(
            nome.value.strip(),
            Auxiliares.limpar_cpf(cpf.value),
            data_formatada.strftime("%Y-%m-%d"),
            telefone.value.strip(),
            email.value.strip(),
            tipo_usuario.value,
            senha_hash
        )
        cadastro_msg.value = "Cadastro realizado com sucesso! Faça login."
        page.update()

    # INTERFACE
    aba_login = ft.Column([
        ft.Text("Login", size=20, weight=ft.FontWeight.BOLD),
        login_cpf,
        login_senha,
        ft.ElevatedButton("Entrar", on_click=realizar_login),
        login_msg
    ], spacing=10)

    aba_cadastro = ft.Column([
        ft.Text("Cadastro", size=20, weight=ft.FontWeight.BOLD),
        nome,
        cpf,
        data_nasc,
        telefone,
        email,
        tipo_usuario,
        senha,
        ft.ElevatedButton("Cadastrar", on_click=realizar_cadastro),
        cadastro_msg
    ], spacing=10)

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Login", content=aba_login),
            ft.Tab(text="Cadastro", content=aba_cadastro)
        ]
    )

    # ⬇️ Retorna a View em vez de adicionar diretamente na página
    return ft.View(
        route="/",
        controls=[tabs]
    )
