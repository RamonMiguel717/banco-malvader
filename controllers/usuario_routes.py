from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from repository.usuarioDAO import UsuarioRepository
from utils.auxiliares import gerar_otp, validar_otp

usuario_bp = Blueprint('usuario', __name__)
otp_codes = {}  # Armazena OTPs temporários por CPF

# Página inicial
@usuario_bp.route('/')
def inicio():
    return render_template('inicio.html')

@usuario_bp.route('/sistema')
def sistema():
    return render_template('sistema.html')

# Rota de login (GET e POST)
@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form['cpf']
        senha = request.form['senha']

        usuario = UsuarioRepository.autenticar_usuario(cpf, senha)
        if usuario:
            session['usuario'] = usuario
            otp = gerar_otp(cpf)  # Gera OTP com base no CPF
            otp_codes[cpf] = otp  # Salva OTP temporariamente
            session['cpf'] = cpf  # Salva CPF na sessão
            print(f"OTP gerado para {cpf}: {otp}")  # Somente para testes

            return redirect(url_for('usuario.validar_otp_view'))
        else:
            flash('CPF ou senha incorretos.')
            return redirect(url_for('usuario.login'))

    return render_template('login.html')

# Rota de validação de OTP (visual)
@usuario_bp.route('/validar_otp', methods=['GET', 'POST'])
def validar_otp_view():
    if request.method == 'POST':
        otp_digitado = request.form.get('otp')
        cpf = session.get('cpf')

        if validar_otp(otp_codes.get(cpf), otp_digitado):
            usuario = session.get('usuario')
            flash("Login realizado com sucesso!", "success")
            if usuario['tipo'] == 'cliente':
                return redirect(url_for('cliente.menu_cliente'))
            else:
                return redirect(url_for('funcionario.menu_funcionario'))
        else:
            flash('OTP incorreto.')

    return render_template('validacao_otp.html')

# API para geração de OTP (JSON)
@usuario_bp.route('/gerar-otp', methods=['POST'])
def rota_gerar_otp():
    data = request.json
    cpf = data.get('cpf')
    if not cpf:
        return jsonify({'erro': 'CPF é obrigatório'}), 400

    otp = gerar_otp(cpf)
    otp_codes[cpf] = otp
    print(f"OTP gerado (API): {otp}")  # Em produção, remova
    return jsonify({'mensagem': 'OTP gerado com sucesso'})  # Nunca envie o OTP no JSON real

# API para validação de OTP (JSON)
@usuario_bp.route('/validar-otp', methods=['POST'])
def rota_validar_otp():
    data = request.json
    cpf = data.get('cpf')
    otp = data.get('otp')

    if not cpf or not otp:
        return jsonify({'erro': 'CPF e OTP são obrigatórios'}), 400

    if validar_otp(otp_codes.get(cpf), otp):
        return jsonify({'mensagem': 'OTP válido'})
    return jsonify({'mensagem': 'OTP inválido ou expirado'}), 400

# Logout
@usuario_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('usuario.login'))
