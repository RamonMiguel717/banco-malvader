import flet as ft
from flet import colors

class ExtratoView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/cliente/extrato")
        self.page = page
        self.build_view()

    def build_view(self):
        # Simulação de dados de extrato
        transacoes = [
            {"data": "01/01/2023", "descricao": "Depósito", "valor": "R$ 1.000,00"},
            {"data": "02/01/2023", "descricao": "Saque", "valor": "R$ -200,00"},
            {"data": "03/01/2023", "descricao": "Transferência", "valor": "R$ -150,00"}
        ]
        
        self.controls = [
            ft.AppBar(
                title=ft.Text("Extrato"),
                bgcolor=colors.BLUE_700,
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.page.go("/cliente")
                )
            ),
            ft.ListView(
                controls=[
                    ft.ListTile(
                        title=ft.Text(t["descricao"]),
                        subtitle=ft.Text(t["data"]),
                        trailing=ft.Text(t["valor"], 
                                       color=colors.GREEN if "R$ -" not in t["valor"] else colors.RED)
                    ) for t in transacoes
                ],
                expand=True
            )
        ]

class TransferenciaView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/cliente/transferir")
        self.page = page
        self.build_view()

    def build_view(self):
        self.conta_destino = ft.TextField(label="Conta Destino")
        self.valor = ft.TextField(label="Valor", keyboard_type=ft.KeyboardType.NUMBER)
        self.descricao = ft.TextField(label="Descrição")
        
        self.controls = [
            ft.AppBar(
                title=ft.Text("Transferência"),
                bgcolor=colors.BLUE_700,
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.page.go("/cliente")
                )
            ),
            ft.Column(
                controls=[
                    self.conta_destino,
                    self.valor,
                    self.descricao,
                    ft.ElevatedButton(
                        text="Transferir",
                        on_click=self.realizar_transferencia,
                        width=200
                    )
                ],
                spacing=20,
                padding=20
            )
        ]
    
    async def realizar_transferencia(self, e):
        if not all([self.conta_destino.value, self.valor.value]):
            self.mostrar_erro("Preencha todos os campos obrigatórios")
            return
        
        try:
            valor = float(self.valor.value)
            if valor <= 0:
                raise ValueError
        except:
            self.mostrar_erro("Valor inválido")
            return
        
        # Aqui você implementaria a transferência no backend
        self.mostrar_sucesso("Transferência realizada com sucesso")
        self.page.go("/cliente")

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