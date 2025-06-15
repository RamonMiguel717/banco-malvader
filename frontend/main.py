import flet as ft
from frontend.login_cadastro import login_cadastro_page
from frontend.validar_otp import valida_otp_page
from frontend.home import home_page

def main(page: ft.Page):
    def route_change(e):
        page.views.clear()  # opcional, só se usar views
        page.controls.clear()  # limpa todos os controles da página (elementos visuais)

        if page.route == "/":
            login_cadastro_page(page)  # adiciona elementos na página
        elif page.route == "/validar_otp":
            valida_otp_page(page)
        elif page.route == "/home":
            home_page(page)

        page.update()  # atualiza a interface

    page.on_route_change = route_change
    page.go(page.route or "/")  # garante que a rota inicial seja carregada

