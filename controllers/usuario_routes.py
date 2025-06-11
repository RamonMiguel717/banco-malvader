from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from repository.usuarioDAO import UsuarioRepository
from utils.auxiliares import gerar_otp, validar_otp, limpar_cpf
from services.cliente_services import ClienteServices
from utils.validator import Validator

usuario_bp = Blueprint('usuario', __name__)
otp_codes = {}  # Armazena OTPs temporários por CPF

# Página inicial
@usuario_bp.route('/')
def inicio_usuario():
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
        tipo_acesso = request.form.get('tipo_acesso', 'cliente')

        usuario = UsuarioRepository.autenticar_usuario(cpf, senha, tipo_acesso)
        if usuario:
            session['usuario'] = usuario
            otp = gerar_otp(cpf)
            otp_codes[cpf] = otp
            session['cpf'] = cpf
            session['tipo_acesso'] = tipo_acesso

            return redirect(url_for('usuario.validar_otp_view'))
        else:
            flash('CPF ou senha incorretos.', 'error')
            return redirect(url_for('usuario.login'))

    return render_template('login.html')

# Rota de cadastro (GET e POST)
@usuario_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        try:
            dados = {
                'nome': request.form.get('nome'),
                'cpf': request.form.get('cpf'),
                'data_nascimento': request.form.get('data_nascimento'),
                'senha': request.form.get('senha'),
                'telefone': request.form.get('telefone'),
                'email': request.form.get('email'),
                'tipo_usuario': 'CLIENTE'
            }

            # Validação do CPF antes de criar a conta
            cpf_limpo = limpar_cpf(dados['cpf'])
            validacao_cpf = Validator.validate_cpf(cpf_limpo)
            
            if not validacao_cpf['valido']:
                raise ValueError("CPF inválido. Por favor, insira um CPF válido.")

            # Se o CPF for válido, prossegue com o cadastro
            ClienteServices.create_account(**dados)
            return jsonify({
                'success': True,
                'message': 'Cadastro realizado com sucesso!',
                'redirect': url_for('usuario.login', message='Cadastro realizado com sucesso!', type='success')
            })
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro ao cadastrar: {str(e)}'
            }), 500

    return render_template('cadastro.html')

# Rota de validação de OTP
@usuario_bp.route('/validar_otp', methods=['GET', 'POST'])
def validar_otp_view():
    if 'usuario' not in session:
        return redirect(url_for('usuario.login'))

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
            flash('OTP incorreto ou expirado.', 'error')

    return render_template('validacao_otp.html')

# API para OTP
@usuario_bp.route('/gerar-otp', methods=['POST'])
def rota_gerar_otp():
    data = request.json
    cpf = data.get('cpf')
    if not cpf:
        return jsonify({'erro': 'CPF é obrigatório'}), 400

    otp = gerar_otp(cpf)
    otp_codes[cpf] = otp
    return jsonify({'mensagem': 'OTP gerado com sucesso'})

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
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('usuario.login'))

# Rota para a tela inicial (casinha)
@usuario_bp.route('/inicio')
def inicio():
    return redirect(url_for('usuario.inicio'))