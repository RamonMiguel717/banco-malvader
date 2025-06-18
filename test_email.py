from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email_remetente = os.getenv('EMAIL_REMETENTE')
senha_email = os.getenv('EMAIL_SENHA')

print(f"Email: {email_remetente}")
print(f"Senha: {senha_email}")
print("EMAIL_REMETENTE:", os.getenv("EMAIL_REMETENTE"))
print("EMAIL_SENHA:", os.getenv("EMAIL_SENHA"))


def enviar_email():
    smtp_servidor = 'smtp.gmail.com'
    smtp_porta = 465

    destinatario = "ramonmiguel777@gmail.com"
    assunto = "Teste de envio"
    corpo = "Este é um teste de envio de e-mail pelo Banco Malvader."

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = email_remetente
    msg['To'] = destinatario
    msg.set_content(corpo)

    contexto = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_servidor, smtp_porta, context=contexto) as server:
            server.login(email_remetente, senha_email)
            server.send_message(msg)
            print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

enviar_email()
