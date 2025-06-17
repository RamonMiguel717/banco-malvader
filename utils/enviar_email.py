import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_otp_email(destinatario_email: str, nome_usuario: str, otp_codigo: str):
    smtp_servidor = 'smtp.gmail.com'
    smtp_porta = 465  # Porta SSL
    email_remetente = os.getenv('EMAIL_REMETENTE')
    senha_email = os.getenv('EMAIL_SENHA')

    # Corpo do e-mail
    assunto = 'Seu código OTP - Banco Malvader'
    corpo = f"""
    Olá {nome_usuario},

    Seu código OTP é: {otp_codigo}

    Este código é válido por 5 minutos. 
    Caso você não tenha solicitado, ignore este e-mail.

    Atenciosamente,
    Banco Malvader
    """

    # Cria a mensagem
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = email_remetente
    msg['To'] = destinatario_email
    msg.set_content(corpo)

    # Envia o e-mail via conexão segura SSL
    contexto = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_servidor, smtp_porta, context=contexto) as server:
            server.login(email_remetente, senha_email)
            server.send_message(msg)
            print(f"E-mail enviado com sucesso para {destinatario_email}")
            return True
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")
        return False
