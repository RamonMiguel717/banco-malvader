import flet as ft
import requests

BASE_URL = "http://localhost:5000"

def main(page: ft.Page):
    page.title = "Sistema Bancário"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    
    def route_change(route):
        page.views.clear()
        
        # Página de login
        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.BLUE),
                        ft.TextField(label="CPF"),
                        ft.TextField(label="Senha", password=True),
                        ft.ElevatedButton("Entrar", on_click=login),
                        ft.TextButton("Registrar", on_click=lambda _: page.go("/registrar"))
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
        
        # Página de registro
        elif page.route == "/registrar":
            page.views.append(
                ft.View(
                    "/registrar",
                    [
                        ft.AppBar(title=ft.Text("Registro"), bgcolor=ft.colors.BLUE),
                        ft.TextField(label="Nome"),
                        ft.TextField(label="CPF"),
                        ft.TextField(label="Senha", password=True),
                        ft.ElevatedButton("Registrar", on_click=registrar),
                        ft.TextButton("Voltar para Login", on_click=lambda _: page.go("/login"))
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
        
        # Página principal (dashboard)
        elif page.route == "/dashboard":
            page.views.append(
                ft.View(
                    "/dashboard",
                    [
                        ft.AppBar(title=ft.Text("Dashboard"), bgcolor=ft.colors.BLUE),
                        ft.Text("Bem-vindo ao sistema bancário!"),
                        ft.ElevatedButton("Minhas Contas", on_click=lambda _: page.go("/contas")),
                        ft.ElevatedButton("Sair", on_click=logout)
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            )
        
        page.update()
    
    def login(e):
        # Implementar chamada para o backend
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "cpf": "12345678901",  # Substituir pelos valores reais
            "senha": "senha123"
        })
        
        if response.status_code == 200:
            page.go("/dashboard")
        else:
            # Mostrar mensagem de erro
            pass
    
    def registrar(e):
        # Implementar chamada para o backend
        response = requests.post(f"{BASE_URL}/auth/registrar", json={
            "nome": "Novo Usuário",  # Substituir pelos valores reais
            "cpf": "12345678901",
            "senha": "senha123"
        })
        
        if response.status_code == 201:
            page.go("/login")
        else:
            # Mostrar mensagem de erro
            pass
    
    def logout(e):
        page.go("/login")
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

ft.app(target=main)