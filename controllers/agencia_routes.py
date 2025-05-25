from flask import Blueprint, request, jsonify
from repository.banco_dao import AgenciaRepository

endereco_bp = Blueprint('endereco',__name__,url_prefix='/endereco')

@endereco_bp.route('/',methods = ['POST'])
def inserir_agencia():
    data = request.json
    AgenciaRepository.insert_agencia(**data)
    return jsonify({"mensagem:":"agencia criada com sucesso"}),201