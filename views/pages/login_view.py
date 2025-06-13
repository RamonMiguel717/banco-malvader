import flet as ft
from flet import colors
from views.pages.cadastro_view import CadastroPage

class LoginPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/login")
        self.page = page
        self.build_view()

    def build_view(self):
        self.cpf_field = ft.TextField(
            label="CPF",
            hint_text="Digite seu CPF",
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.senha_field = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True
        )
        
        self.login_button = ft.ElevatedButton(
            text="Entrar",
            on_click=self.fazer_login,
            width=200
        )
        
        self.registro_button = ft.TextButton(
            text="Criar uma conta",
            on_click=lambda _: self.page.go("/registrar")
        )
        
        self.controls = [
            ft.AppBar(title=ft.Text("Login"), bgcolor=colors.BLUE_700),
            ft.Image(src="/static/img/logo.png", width=150, height=150),
            ft.Column(
                controls=[
                    self.cpf_field,
                    self.senha_field,
                    self.login_button,
                    self.registro_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        ]
    
    async def fazer_login(self, e):
        if not self.cpf_field.value or not self.senha_field.value:
            self.mostrar_erro("Preencha todos os campos")
            return
        
        # Aqui você implementaria a chamada ao backend
        self.page.go("/dashboard")

    def mostrar_erro(self, mensagem):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=colors.RED
        )
        self.page.snack_bar.open = True
        self.page.update()