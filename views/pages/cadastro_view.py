import flet as ft
from flet import colors
from utils.validator import validar_cpf, validar_email

class CadastroPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/registrar")
        self.page = page
        self.build_view()

    def build_view(self):
        self.nome_field = ft.TextField(label="Nome Completo")
        self.cpf_field = ft.TextField(label="CPF", keyboard_type=ft.KeyboardType.NUMBER)
        self.email_field = ft.TextField(label="Email", keyboard_type=ft.KeyboardType.EMAIL)
        self.senha_field = ft.TextField(label="Senha", password=True)
        self.confirma_senha_field = ft.TextField(label="Confirmar Senha", password=True)
        
        self.registrar_button = ft.ElevatedButton(
            text="Registrar",
            on_click=self.registrar_usuario,
            width=200
        )
        
        self.login_button = ft.TextButton(
            text="Já tem conta? Faça login",
            on_click=lambda _: self.page.go("/login")
        )
        
        self.controls = [
            ft.AppBar(title=ft.Text("Cadastro"), bgcolor=colors.BLUE_700),
            ft.Column(
                controls=[
                    self.nome_field,
                    self.cpf_field,
                    self.email_field,
                    self.senha_field,
                    self.confirma_senha_field,
                    self.registrar_button,
                    self.login_button
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    
    async def registrar_usuario(self, e):
        if not all([self.nome_field.value, self.cpf_field.value, 
                   self.email_field.value, self.senha_field.value]):
            self.mostrar_erro("Preencha todos os campos")
            return
            
        if not validar_cpf(self.cpf_field.value):
            self.mostrar_erro("CPF inválido")
            return
            
        if not validar_email(self.email_field.value):
            self.mostrar_erro("Email inválido")
            return
            
        if self.senha_field.value != self.confirma_senha_field.value:
            self.mostrar_erro("As senhas não coincidem")
            return
        
        # Aqui você implementaria a chamada ao backend
        self.page.go("/otp")

    def mostrar_erro(self, mensagem):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=colors.RED
        )
        self.page.snack_bar.open = True
        self.page.update()