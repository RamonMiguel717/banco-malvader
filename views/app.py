import flet as ft
from views.pages.login_view import LoginPage
from views.pages.cadastro_view import CadastroPage
from views.pages.otp_view import OtpPage
from views.pages.dashboard import MenuClientePage, MenuFuncionarioPage
from views.pages.menu_cliente import ExtratoView, TransferenciaView

def main(page: ft.Page):
    page.title = "Banco Malvader"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    def route_change(route):
        page.views.clear()
        
        if route == "/login":
            page.views.append(LoginPage(page))
        elif route == "/registrar":
            page.views.append(CadastroPage(page))
        elif route == "/otp":
            page.views.append(OtpPage(page))
        elif route == "/cliente":
            page.views.append(MenuClientePage(page))
        elif route == "/cliente/extrato":
            page.views.append(ExtratoView(page))
        elif route == "/cliente/transferir":
            page.views.append(TransferenciaView(page))
        elif route == "/funcionario":
            page.views.append(MenuFuncionarioPage(page))
        
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

ft.app(target=main, view=ft.AppView.WEB_BROWSER)