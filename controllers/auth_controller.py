from flask import Blueprint, request, jsonify
from repository.usuarioDAO import get_usuario_by_cpf, insert_usuario
from services.cliente_services import registrar_cliente
from utils.validator import validar_cpf, validar_email
from utils.criptografia_senha import gerar_hash_senha

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    dados = request.get_json()
    
    # Validações
    if not validar_cpf(dados.get('cpf')):
        return jsonify({"erro": "CPF inválido"}), 400
    
    if not validar_email(dados.get('email')):
        return jsonify({"erro": "Email inválido"}), 400
    
    # Verifica se usuário já existe
    if get_usuario_by_cpf(dados['cpf']):
        return jsonify({"erro": "CPF já cadastrado"}), 400
    
    try:
        # Cria hash da senha
        senha_hash = gerar_hash_senha(dados['senha'])
        
        # Cria usuário
        usuario = insert_usuario(
            nome=dados['nome'],
            cpf=dados['cpf'],
            email=dados['email'],
            senha_hash=senha_hash
        )
        
        # Registra como cliente
        cliente = registrar_cliente(usuario.id)
        
        return jsonify({
            "mensagem": "Registro realizado com sucesso",
            "usuario_id": usuario.id,
            "cliente_id": cliente.id
        }), 201
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    usuario = get_usuario_by_cpf(dados['cpf'])
    
    if not usuario:
        return jsonify({"erro": "CPF ou senha inválidos"}), 401
    
    from utils.criptografia_senha import verificar_senha
    if not verificar_senha(usuario.senha_hash, dados['senha']):
        return jsonify({"erro": "CPF ou senha inválidos"}), 401
    
    return jsonify({
        "mensagem": "Login bem-sucedido",
        "usuario_id": usuario.id,
        "nome": usuario.nome
    }), 200