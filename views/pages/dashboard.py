import flet as ft
from flet import colors, icons
from typing import Optional
from flet import Page

class MenuClientePage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/cliente")
        self.page = page
        self.build_view()

    def build_view(self):
        self.saldo_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Saldo Disponível", size=16),
                        ft.Text("R$ 1.234,56", size=24, weight=ft.FontWeight.BOLD)
                    ],
                    spacing=10
                ),
                padding=20,
                width=300
            )
        )
        
        self.controls = [
            ft.AppBar(
                title=ft.Text("Dashboard Cliente"),
                bgcolor=ft.colors.BLUE_700,
                actions=[
                    ft.IconButton(icons.LOGOUT, on_click=self.sair)
                ]
            ),
            ft.Row(
                controls=[self.saldo_card],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.GridView(
                controls=[
                    self.menu_button("Extrato", icons.RECEIPT),
                    self.menu_button("Transferir", icons.TRANSFER_WITHIN_A_STATION),
                    self.menu_button("Depositar", icons.ACCOUNT_BALANCE_WALLET),
                    self.menu_button("Cartões", icons.CREDIT_CARD),
                    self.menu_button("Perfil", icons.PERSON),
                    self.menu_button("Ajuda", icons.HELP)
                ],
                runs_count=2,
                max_extent=150,
                spacing=10,
                run_spacing=10,
                padding=20
            )
        ]
    
    def menu_button(self, texto: str, icone: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icone, size=40),
                    ft.Text(texto)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            alignment=ft.alignment.center,
            width=150,
            height=150,
            bgcolor=colors.BLUE_50,
            border_radius=10,
            on_click=lambda e: self.abrir_tela(texto.lower())
        )
    
    def abrir_tela(self, tela: str):
        self.page.go(f"/cliente/{tela}")
    
    def sair(self, e):
        self.page.go("/login")

class MenuFuncionarioPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/funcionario")
        self.page = page
        self.build_view()

    def build_view(self):
        self.controls = [
            ft.AppBar(
                title=ft.Text("Dashboard Funcionário"),
                bgcolor=colors.BLUE_700,
                actions=[
                    ft.IconButton(icons.LOGOUT, on_click=self.sair)
                ]
            ),
            ft.GridView(
                controls=[
                    self.menu_button("Clientes", icons.PEOPLE),
                    self.menu_button("Contas", icons.ACCOUNT_BALANCE),
                    self.menu_button("Transações", icons.PAYMENTS),
                    self.menu_button("Relatórios", icons.ANALYTICS),
                    self.menu_button("Configurações", icons.SETTINGS)
                ],
                runs_count=2,
                max_extent=150,
                spacing=10,
                run_spacing=10,
                padding=20
            )
        ]
    
    def menu_button(self, texto: str, icone: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icone, size=40),
                    ft.Text(texto)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            alignment=ft.alignment.center,
            width=150,
            height=150,
            bgcolor=colors.BLUE_50,
            border_radius=10,
            on_click=lambda e: self.abrir_tela(texto.lower())
        )
    
    def abrir_tela(self, tela: str):
        self.page.go(f"/funcionario/{tela}")
    
    def sair(self, e):
        self.page.go("/login")