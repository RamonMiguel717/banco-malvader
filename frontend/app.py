from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from backend.utils.auxiliares import Auxiliares
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['BACKEND_URL'] = 'http://localhost:5000'

# Rota principal
@app.route('/')
def index():
    return render_template('auth/login.html')

# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tipo_usuario = request.form.get('tipo_usuario')
        login = request.form.get('login')
        senha = request.form.get('senha')
        
        # Chamar API do backend para autenticação
        try:
            response = requests.post(
                f"{app.config['BACKEND_URL']}/auth/login",
                json={
                    'tipo_usuario': tipo_usuario,
                    'login': login,
                    'senha': senha
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                session['user_info'] = data
                session['tipo_usuario'] = tipo_usuario
                
                # Redirecionar para página de OTP
                return redirect(url_for('otp_verification'))
            else:
                return render_template('auth/login.html', error="Credenciais inválidas")
        
        except requests.exceptions.RequestException:
            return render_template('auth/login.html', error="Erro de conexão com o servidor")
    
    return render_template('auth/login.html')

@app.route('/otp', methods=['GET', 'POST'])
def otp_verification():
    if 'user_info' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        otp = request.form.get('otp')
        
        # Verificar OTP no backend
        try:
            response = requests.post(
                f"{app.config['BACKEND_URL']}/auth/verify-otp",
                json={
                    'user_id': session['user_info']['id'],
                    'otp': otp
                }
            )
            
            if response.status_code == 200:
                # Login bem-sucedido, redirecionar para dashboard apropriado
                if session['tipo_usuario'] == 'cliente':
                    return redirect(url_for('cliente_dashboard'))
                else:
                    return redirect(url_for('funcionario_dashboard'))
            else:
                return render_template('auth/otp.html', error="OTP inválido ou expirado")
        
        except requests.exceptions.RequestException:
            return render_template('auth/otp.html', error="Erro de conexão com o servidor")
    
    return render_template('auth/otp.html')

# Rotas para clientes
@app.route('/cliente/dashboard')
def cliente_dashboard():
    if 'user_info' not in session or session['tipo_usuario'] != 'cliente':
        return redirect(url_for('login'))
    
    # Obter informações da conta do cliente
    try:
        response = requests.get(
            f"{app.config['BACKEND_URL']}/clientes/{session['user_info']['id']}/contas",
            headers={'Authorization': f"Bearer {session['user_info']['token']}"}
        )
        
        contas = response.json() if response.status_code == 200 else []
        
        return render_template('cliente/dashboard.html', contas=contas)
    
    except requests.exceptions.RequestException:
        return render_template('cliente/dashboard.html', error="Erro ao carregar dados")

# Rotas para funcionários (similar às rotas de cliente, mas com mais funcionalidades)
@app.route('/funcionario/dashboard')
def funcionario_dashboard():
    if 'user_info' not in session or session['tipo_usuario'] == 'cliente':
        return redirect(url_for('login'))
    
    # Verificar nível de acesso
    nivel_acesso = session['user_info'].get('nivel_acesso', 0)
    
    return render_template('funcionario/dashboard.html', nivel_acesso=nivel_acesso)

# API para integração com Flet
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(path):
    if 'user_info' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    try:
        headers = {
            'Authorization': f"Bearer {session['user_info']['token']}",
            'Content-Type': 'application/json'
        }
        
        url = f"{app.config['BACKEND_URL']}/{path}"
        
        if request.method == 'GET':
            response = requests.get(url, headers=headers, params=request.args)
        elif request.method == 'POST':
            response = requests.post(url, headers=headers, json=request.json)
        elif request.method == 'PUT':
            response = requests.put(url, headers=headers, json=request.json)
        elif request.method == 'DELETE':
            response = requests.delete(url, headers=headers)
        
        return jsonify(response.json()), response.status_code
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)