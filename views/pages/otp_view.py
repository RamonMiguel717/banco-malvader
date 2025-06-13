import flet as ft
from flet import colors

class OtpPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/otp")
        self.page = page
        self.build_view()

    def build_view(self):
        self.otp_field = ft.TextField(
            label="Código de Verificação",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200
        )
        
        self.verificar_button = ft.ElevatedButton(
            text="Verificar",
            on_click=self.verificar_otp,
            width=200
        )
        
        self.reenviar_button = ft.TextButton(
            text="Reenviar código",
            on_click=self.reenviar_otp
        )
        
        self.controls = [
            ft.AppBar(title=ft.Text("Verificação"), bgcolor=colors.BLUE_700),
            ft.Column(
                controls=[
                    ft.Text("Enviamos um código de 6 dígitos para seu email"),
                    self.otp_field,
                    self.verificar_button,
                    self.reenviar_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        ]
    
    async def verificar_otp(self, e):
        if len(self.otp_field.value) != 6 or not self.otp_field.value.isdigit():
            self.mostrar_erro("Código inválido")
            return
        
        # Aqui você implementaria a verificação no backend
        self.page.go("/dashboard")

    async def reenviar_otp(self, e):
        # Implementar reenvio de OTP
        self.mostrar_sucesso("Código reenviado com sucesso")

    def mostrar_erro(self, mensagem):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=colors.RED
        )
        self.page.snack_bar.open = True
        self.page.update()
        
    def mostrar_sucesso(self, mensagem):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=colors.GREEN
        )
        self.page.snack_bar.open = True
        self.page.update()