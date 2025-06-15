import flet as ft

def home_page(page: ft.Page):
    page.title = "Banco Malvader - Home"
    cpf = page.session.get("cpf")
    if not cpf:
        page.go("/")
        return

    page.add(
        ft.Text(f"Bem-vindo ao sistema, CPF: {cpf}")
    )
