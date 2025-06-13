from models.database import db
from datetime import datetime

class Conta(db.Model):
    __tablename__ = 'contas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    agencia = db.Column(db.String(10), nullable=False)
    saldo = db.Column(db.Float, default=0.0)
    tipo = db.Column(db.String(20), nullable=False)  # 'corrente', 'poupança', etc.
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativa = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    transacoes = db.relationship('Transacao', backref='conta', lazy=True)