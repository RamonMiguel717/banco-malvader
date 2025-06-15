import threading
import time
import flet as ft
from frontend.main import main  # ou apenas `from main import main`, se estiver na raiz
from backend.api import create_app

def run_api():
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

def start():
    # Roda a API Flask em segundo plano
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    time.sleep(1)  # Aguarda a API subir
    ft.app(target=main, view=ft.WEB_BROWSER)  # ✅ CORRETO: sem parênteses

if __name__ == "__main__":
    start()
