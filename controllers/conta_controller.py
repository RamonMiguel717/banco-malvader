from flask import Blueprint, request, jsonify
from repository.contasDAO import insert_conta, get_contas_by_usuario_id
from services.conta_services import realizar_deposito_service
from utils.validator import validar_numero_conta

conta_bp = Blueprint('conta', __name__)

@conta_bp.route('/<int:usuario_id>/contas', methods=['POST'])
def criar_nova_conta(usuario_id):
    dados = request.get_json()
    
    if not validar_numero_conta(dados.get('numero')):
        return jsonify({"erro": "Número de conta inválido"}), 400
    
    try:
        conta = insert_conta(
            numero=dados['numero'],
            agencia=dados['agencia'],
            tipo=dados['tipo'],
            usuario_id=usuario_id
        )
        
        return jsonify({
            "mensagem": "Conta criada com sucesso",
            "conta_id": conta.id
        }), 201
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@conta_bp.route('/<int:conta_id>/deposito', methods=['POST'])
def depositar(conta_id):
    valor = request.json.get('valor')
    
    if not valor or float(valor) <= 0:
        return jsonify({"erro": "Valor inválido"}), 400
    
    try:
        transacao = realizar_deposito_service(conta_id, float(valor))
        
        return jsonify({
            "mensagem": "Depósito realizado",
            "novo_saldo": transacao.conta.saldo,
            "transacao_id": transacao.id
        }), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500