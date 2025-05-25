from flask import Blueprint, request, jsonify
from repository.banco_dao import EnderecoRepository

endereco_bp = Blueprint('endereco_bp', __name__)

# Endereco
@endereco_bp.route("/enderecos", methods=["GET"])
def listar_enderecos():
    return jsonify(EnderecoRepository.list_enderecos()), 200

@endereco_bp.route("/enderecos", methods=["POST"])
def criar_endereco():
    data = request.json
    EnderecoRepository.insert_endereco(**data)
    return jsonify({"mensagem": "Endereço criado com sucesso"}), 201

@endereco_bp.route("/enderecos/<int:id>", methods=["PUT"])
def atualizar_endereco(id):
    data = request.json
    EnderecoRepository.update_endereco(id, **data)
    return jsonify({"mensagem": "Endereço atualizado"}), 200

@endereco_bp.route("/enderecos/<int:id>", methods=["DELETE"])
def deletar_endereco(id):
    EnderecoRepository.delete_endereco(id)
    return jsonify({"mensagem": "Endereço deletado"}), 200


