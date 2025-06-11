from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from repository.clienteDAO import ClienteRepository

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/', methods=['GET'])
def listar_clientes():
    """List all clients in JSON format"""
    try:
        clientes = ClienteRepository.list_clientes()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/<int:id_cliente>', methods=['GET'])
def detalhes_cliente(id_cliente):
    """Render client details page"""
    cliente = ClienteRepository.get_cliente_by_id(id_cliente)
    if cliente:
        return render_template('cliente/detalhes_cliente.html', cliente=cliente)
    else:
        return "Cliente não encontrado", 404

@cliente_bp.route('/novo', methods=['GET'])
def formulario_novo_cliente():
    """Render form to create a new client"""
    return render_template('cliente/novo_cliente.html')

@cliente_bp.route('/', methods=['POST'])
def criar_cliente():
    dados = request.json
    try:
        ClienteRepository.insert_cliente(
            id_usuario=dados['id_usuario'],
            score_credito=dados.get('score_credito', 0)
        )
        return jsonify({'mensagem': 'Cliente criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@cliente_bp.route('/<int:id_cliente>', methods=['PUT'])
def atualizar_cliente(id_cliente):
    dados = request.json
    try:
        ClienteRepository.update_cliente(id_cliente, dados['score_credito'])
        return jsonify({'mensagem': 'Cliente atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@cliente_bp.route('/<int:id_cliente>', methods=['DELETE'])
def deletar_cliente(id_cliente):
    try:
        ClienteRepository.delete_cliente(id_cliente)
        return jsonify({'mensagem': 'Cliente deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

