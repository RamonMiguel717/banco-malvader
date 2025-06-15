import flet as ft
from backend.utils.auxiliares import Auxiliares

def valida_otp_page(page: ft.Page):
    page.title = "Validação OTP - Banco Malvader"

    cpf = page.session.get("cpf")
    if not cpf:
        page.go("/")  # Sem login? volta para o início
        return

    otp_input = ft.TextField(label="Digite o código OTP", width=300)
    otp_msg = ft.Text(value="", color=ft.Colors.RED, size=12)

    def verificar_otp(e):
        if Auxiliares.validar_otp(cpf, otp_input.value):
            otp_msg.value = "Acesso autorizado!"
            otp_msg.color = ft.Colors.GREEN
            # Redireciona para a página final
            page.go("/home")  # ou /painel, como preferir
        else:
            otp_msg.value = "OTP inválido ou expirado."
            otp_msg.color = ft.Colors.RED
        page.update()

    page.add(
        ft.Column([
            ft.Text("Validação OTP", size=20, weight=ft.FontWeight.BOLD),
            otp_input,
            ft.ElevatedButton("Verificar", on_click=verificar_otp),
            otp_msg
        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
