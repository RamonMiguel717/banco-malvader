import flet as ft
import requests

BASE_URL = "http://localhost:5000"

class BancoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.usuario_logado = None
        self.token_acesso = None
        
        # Rotas
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go("/login")
    
    def setup_page(self):
        self.page.title = "Banco Malvader"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = 20
    
    def route_change(self, route):
        self.page.views.clear()
        
        if route == "/login":
            self.login_view()
        elif route == "/registrar":
            self.registro_view()
        elif route == "/dashboard":
            self.dashboard_view()
        
        self.page.update()
    
    def view_pop(self, view):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
    
    def login_view(self):
        self.cpf_field = ft.TextField(label="CPF")
        self.senha_field = ft.TextField(label="Senha", password=True)
        
        view = ft.View(
            "/login",
            [
                ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.BLUE_700),
                ft.Image(src="static/img/logo.png", width=150, height=150),
                self.cpf_field,
                self.senha_field,
                ft.ElevatedButton("Entrar", on_click=self.fazer_login),
                ft.TextButton("Criar conta", on_click=lambda _: self.page.go("/registrar"))
            ],
            spacing=20
        )
        self.page.views.append(view)
    
    async def fazer_login(self, e):
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "cpf": self.cpf_field.value,
                "senha": self.senha_field.value
            }
        )
        
        if response.status_code == 200:
            dados = response.json()
            self.usuario_logado = dados['usuario']
            self.token_acesso = dados.get('token')
            self.page.go("/dashboard")
        else:
            erro = response.json().get('erro', 'Erro ao fazer login')
            self.page.snack_bar = ft.SnackBar(ft.Text(erro))
            self.page.snack_bar.open = True
            self.page.update()
    
    def registro_view(self):
        # Implementar similar ao login_view
        pass
    
    def dashboard_view(self):
        # Implementar dashboard com menus
        pass

def main(page: ft.Page):
    BancoApp(page)

ft.app(target=main, view=ft.WEB_BROWSER)